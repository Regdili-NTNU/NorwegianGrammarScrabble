#!/usr/bin/env python
# coding: utf-8

import os
import cherrypy
import parser
import json
import random
import urllib, urllib2
import xml.etree.ElementTree as ET
import time

PARSE_ADDRESS = "http://regdili.hf.ntnu.no:8081/malgram/rest/parse"
ERROR_ADDRESS = "http://regdili.hf.ntnu.no:8081/malgram/rest/messages"
GENERATE_ADDRESS = "http://regdili.hf.ntnu.no:8081/bongram/rest/generate"

WORD_BLACKLIST = [
  "period",
  "quest-mark",
  "exclam-mark",
  "comma",
  "colon",
  "semicolon",
  "relcl-comma",
  "s",
  "quest",
]

EXCEPTION_STEM_MAP = {
	"mal_jeg_perspron" : "jeg",
	"mal_meg_perspron" : "meg", 
	"mal_vi_perspron" : "vi",
	"mal_oss_perspron" : "oss",
	"mal_du_perspron" : "du",
	"mal_deg_perspron" : "deg",
	"mal_de_perspron" : "de",
	"mal_dem_perspron" : "dem",
	"mal_hun_perspron" : "hun",
	"mal_henne_perspron" : "henne",
	"mal-sin_refl-pre-poss" : "sin",
	"mal-sin_refl_post-poss" : "sin",
	"mal-si_refl-pre-poss" : "si",
	"mal-si_refl_post-poss" : "si",
	"mal-sitt_refl-pre-poss" : "sitt",
	"mal-sitt_refl_post-poss" : "sitt",
	"mal-sine_refl-pre-poss" : "sine",
	"mal-sine_refl_post-poss" : "sine",
	"mal_og_inf_comp" : "og",
	"mal_å__n-coord" : "å",
	"mal_å_adv-p-coord" : "å",
	"mal_å_v-coord" : "å",
	"mal_å_adj-coord" : "å",
	"mal_seg_for_meg_refl" : "seg",
	"mal_seg_for_deg_refl" : "seg",
	"mal_seg_for_oss_refl" : "seg",
	"mal_seg_for_dere_refl" : "seg",
	}

def read_weighted(filename):
  words = []
  number = 0
  with open(filename, 'r') as wordfile:
    for line_nbr, line in enumerate(wordfile):
      line = line.strip()
      line = line.split()
      if line_nbr == 0:
         number = int(line[0]) 
         continue
      if len(line) == 1:
        words.append(line[0])
      elif len(line) == 3:
        for i in xrange(int(line[-1])):
          words.append(line[0])
  return number, words

word_lists = []
for filename in os.listdir(os.getcwd() + "/words"):
  print "Reading file " + filename
  word_lists.append(read_weighted("words/" + filename))

class GameServer(object):

  def __init__(self):
    self.parses = 0
    self.scores = []

  def call_chain(self, sentence, available_words):
    response = {"original_sentence" : sentence}
    parse_xml = self.call_parse(sentence)

    readings = int(parse_xml.find("readings").text)
    if readings <= 0:
       response["error"] = parse_xml.find("error").text
       return response

    best_index = self.find_best_parse_index(parse_xml, available_words)
    best_parse = self.get_parse_number(parse_xml, best_index)

    used_words = self.find_words_in_syntax_tree(best_parse)
    illegal_words = self.check_words(used_words, available_words)

    if illegal_words:
      if len(illegal_words) == 1:
        response["error"] = 'The word "' + \
          ' '.join(illegal_words).strip() + '" is not available.'
      else:
        response["error"] = 'The words "' + \
          ' '.join(illegal_words).strip() + '" are not available.'
      return response

    response["used_words"] = used_words
    error_xml = self.call_error(best_parse)
    error_messages = self.add_error_messages(error_xml)

    if error_messages:
      response["malfeedback"] = error_messages
      best_mrs = self.get_mrs_number(parse_xml, best_index)
      generate_xml = self.call_generate(best_mrs, sentence)
      generated = generate_xml.find("stm")
      if generated != None:
        response["suggestion"] = generated.text

    response["score"] = len(used_words) - len(error_messages)

    return response

  def call_parse(self, sentence):
    request = {"statement" : sentence, "client" : "pre_scrabble", "readings" : 1}
    request_address = PARSE_ADDRESS + "?" + urllib.urlencode(request)
    response = urllib2.urlopen(request_address).read()
    return ET.fromstring(response)

  # Returns the index of the best parse in the result, defined by how well it
  # matches the words available to the user. 
  def find_best_parse_index(self, parse_xml, available_words):
    best_index = -1
    best_score = 1e10
    for index, syntax_tree in enumerate(parse_xml.iter("syntax-tree")):
      used_words = self.find_words_in_syntax_tree(syntax_tree)
      illegal_words = self.check_words(used_words, available_words)
      if len(illegal_words) == 0:
        return index 
      if len(illegal_words) < best_score:
        best_index = index
        best_score = len(illegal_words) 
    return best_index 
	
  def find_words_in_syntax_tree(self, syntax_tree):
    words = []
    leaf_parent_indices = []
    for terminal in syntax_tree.iter("terminal"):
      leaf_parent_indices.append(terminal.attrib["parent"])
    for node in syntax_tree.iter("node"):
      if node.attrib["id"] in leaf_parent_indices:
        full_word_rule = node.attrib["name"]
        stem = full_word_rule
        if '_' in full_word_rule or '-' in full_word_rule:
          index1 = full_word_rule.index('_') if '_' in full_word_rule else 1e10
          index2 = full_word_rule.index('-') if '-' in full_word_rule else 1e10
          stem = full_word_rule[:min([index1, index2])]
        if full_word_rule in EXCEPTION_STEM_MAP:
          stem = EXCEPTION_STEM_MAP[full_word_rule]
        if not stem in WORD_BLACKLIST:
          words.append(stem.lower())
    return words

  def get_parse_number(self, parse_xml, index):
    for i, syntax_tree in enumerate(parse_xml.iter("syntax-tree")):
      if i == index:
        return syntax_tree 

  def get_mrs_number(self, parse_xml, index):
    for i, syntax_tree in enumerate(parse_xml.iter("mrs")):
      if i == index:
        return syntax_tree 

  def check_words(self, used_words, available_words):
    illegal_words = []
    for used_word in used_words:
      if not used_word in available_words:
        illegal_words.append(used_word)
    return illegal_words

  def call_error(self, syntax_tree):
    request = {"syntax" : ET.tostring(syntax_tree)}
    request_address = ERROR_ADDRESS + "?" + urllib.urlencode(request)
    response = urllib2.urlopen(request_address).read()
    return ET.fromstring(response)

  def add_error_messages(self, error_xml):
    error_messages = []
    for message in error_xml.iter("message"):
      error_messages.append(message.text)
    return error_messages

  def call_generate(self, mrs, sentence):
    request = {"statement" : sentence, "mrs" : ET.tostring(mrs), "client" : "pre_scrabble"}
    request_address = GENERATE_ADDRESS + "?" + urllib.urlencode(request)
    response = urllib2.urlopen(request_address).read()
    return ET.fromstring(response)

  @cherrypy.expose
  @cherrypy.tools.json_in()
  @cherrypy.tools.json_out()
  def parse(self):
    self.parses += 1
    request = cherrypy.request.json
    sentence = request.get("sentence")
    words = request.get("words")
    sentence = sentence.encode("utf-8")
    response = self.call_chain(sentence, words)
    return json.dumps(response)

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def words(self):
    words = []
    for word_list in word_lists:
       words.extend(random.sample(word_list[1], word_list[0]))
    response = {'words' : words}
    return json.dumps(response)

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def count(self):
    return json.dumps({'parses' : self.parses})

  @cherrypy.expose
  @cherrypy.tools.json_in()
  def add_score(self):
    request = cherrypy.request.json
    score = request.get("score")
    username = request.get("username")
    self.scores.append({"score" : score, "user" : username, "timestamp" : time.time()})
    if len(self.scores) > 100:
      self.scores = []

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def get_scores(self):
    response = []
    for score in self.scores:
      response.append(score) 
    return json.dumps({'scores' : response})
    
class WebPage(object):
  pass

cherrypy.config.update({
  'log.access_file' : 'logs/access.log',
  'log.error_file' : 'logs/error.log',
  'server.socket_port' : 5051,
  'server.socket_host' : '0.0.0.0',
  'tools.response_headers.on' : True,
  'tools.response_headers.headers' : [('Access-Control-Allow-Origin', '*')],
})

cherrypy.tree.mount(GameServer(), "/server")
cherrypy.tree.mount(WebPage(), "/page", {"/" : {"tools.staticdir.on" : True, "tools.staticdir.dir" : "/home/regdili/scrabble/malgramweb", "tools.staticdir.index" : "index.html"}})

cherrypy.engine.start()
cherrypy.engine.block()
