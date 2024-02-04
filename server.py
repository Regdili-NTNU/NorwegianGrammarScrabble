#!/usr/bin/env python
# coding: utf-8

import os
import cherrypy
import json
import random
import urllib, urllib2
import xml.etree.ElementTree as ET
import ast
import time

PARSE_ADDRESS = "http://xregdili.hf.ntnu.no:8081/malgram/rest/parse"
ERROR_ADDRESS = "http://xregdili.hf.ntnu.no:8081/malgram/rest/messages"
GENERATE_ADDRESS = "http://xregdili.hf.ntnu.no:8081/bongram/rest/generate"

# PARSE_ADDRESS = "http://192.168.0.122:8081/MalgramRest/parse"
# ERROR_ADDRESS = "http://192.168.0.122:8081/MalgramRest/messages"
# GENERATE_ADDRESS = "http://192.168.0.122:8081/BongramRest/generate"

SCORE_FILE = 'storage/scores.dv'

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

LANGUAGE_NAME_TO_NUMBER_MAP = {
	"en" : 1,
	"pl" : 2,
	"it" : 3,
	"de" : 4,
	"zh" : 5,
	"ar" : 6,
	"bg" : 7,
	"no" : 8,
}

SINGLE_WORD_NOT_FOUND = [
  "The word %s is not available.", 
  "The word %s is not available.", 
  "The word %s is not available.", 
  "The word %s is not available.", 
  "The word %s is not available.", 
  "The word %s is not available.", 
  "The word %s is not available.", 
  "Ordet %s er ikke tilgjengelig denne runden.", 
]

MULTIPLE_WORDS_NOT_FOUND = [
  "The words %s are not available.", 
  "The words %s are not available.", 
  "The words %s are not available.", 
  "The words %s are not available.", 
  "The words %s are not available.", 
  "The words %s are not available.", 
  "The words %s are not available.", 
  "Ordene %s er ikke tilgjengelig denne runden.", 
]

ONE_WEEK = 60 * 60 * 24 * 7

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
        for i in range(int(line[-1])):
          words.append(line[0])
  return number, words

word_lists = []
for filename in os.listdir(os.getcwd() + "/words"):
  print( "Reading file " + filename)
  word_lists.append(read_weighted("words/" + filename))

class GameServer(object):

  def __init__(self):
    self.parses = 0
    self.scores = self.read_scores()

  def read_scores(self):
    scores = []
    with open(SCORE_FILE, 'r') as scorefile:
      for line in scorefile:
        scores.append(ast.literal_eval(line.strip()))
    return scores
	  
  def process_error(self, record):
    index = record.find('lexemes do not span')
    if index > -1:
      beg = record.find('`')
      end = record.find("'")
      if beg > -1 and end > -1:
        return 'Lexicon entry: "'+record[beg+1:end]+'" is missing'
    index = record.find('NOTE: 0 readings')
    if index > -1:
      return 'Ungrammatical in Norwegian'
    return record
	  
  def call_chain(self, sentence, language, available_words):
    response = {"original_sentence" : sentence}
    parse_xml = self.call_parse(sentence)

    readings = int(parse_xml.find("readings").text)
    if readings <= 0:
       response["error"] = self.process_error(parse_xml.find("error").text)
       return response
    best_index = self.find_best_parse_index(parse_xml, available_words)
    best_parse = self.get_parse_number(parse_xml, best_index)

    used_words = self.find_words_in_syntax_tree(best_parse)
    illegal_words = self.check_words(used_words, available_words)

    if illegal_words:
      if len(illegal_words) == 1:
        response["error"] = SINGLE_WORD_NOT_FOUND[LANGUAGE_NAME_TO_NUMBER_MAP[language]-1] % \
          ' '.join(illegal_words).strip()
      else:
        response["error"] = MULTIPLE_WORDS_NOT_FOUND[LANGUAGE_NAME_TO_NUMBER_MAP[language]-1] % \
          ' '.join(illegal_words).strip()
      return response

    response["used_words"] = used_words
    error_xml = self.call_error(best_parse, language)
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
    dict = {"statement" : sentence, "client" : "crab", "readings" : 25}
    data = json.dumps(dict)
    req = urllib2.Request(PARSE_ADDRESS, data=data) 
    response = urllib2.urlopen(req).read()
    return ET.fromstring(response)

  # Returns the index of the best parse in the result, defined by how well it
  # matches the words available to the user. 
  def find_best_parse_index(self, parse_xml, available_words):
    best_index = -1
    best_score = 1e10
    for index, syntax_tree in enumerate(parse_xml.iter("syntaxtree")):
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
    for i, syntax_tree in enumerate(parse_xml.iter("syntaxtree")):
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

  def call_error(self, syntax_tree, language):
    language_number = LANGUAGE_NAME_TO_NUMBER_MAP.get(language)
    if language_number == None: language_number = 1
   
    dict = {"syntax" : ET.tostring(syntax_tree, encoding='utf-8'), "language" : str(language_number)}
    data = json.dumps(dict)
    req = urllib2.Request(ERROR_ADDRESS, data=data) 
    response = urllib2.urlopen(req).read()

    return ET.fromstring(response)

  def add_error_messages(self, error_xml):
    error_messages = []
    if error_xml == "" or error_xml == None:
      return error_messages
    for message in error_xml.iter("message"):
      error_messages.append(message.text)
    return error_messages

  def call_generate(self, mrs, statement):
    dict = {"statement": statement, "mrs": ET.tostring(mrs, encoding='utf-8'), "client": "scrab"}
    data = json.dumps(dict)
    req = urllib2.Request(GENERATE_ADDRESS, data=data) 
    response = urllib2.urlopen(req).read()
    return ET.fromstring(response)
  

  @cherrypy.expose
  @cherrypy.tools.json_in()
  @cherrypy.tools.json_out()
  def parse(self):
    self.parses += 1
    request = cherrypy.request.json
    sentence = request.get("sentence")
    language = request.get("language")
    words = request.get("words")
    sentence = sentence.encode("utf-8")
    response = self.call_chain(sentence, language, words)
    return json.dumps(response)

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def words(self):
    words = []
    for word_list in word_lists:
       words.extend(random.sample(word_list[1], word_list[0]))
    words = sorted(words)
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
    now = time.time()
    self.scores.append({"score" : score, "user" : username, "timestamp" : now})
    self.scores = sorted(self.scores, key=lambda score: score["score"], reverse=True)
    self.scores = [score for i, score in enumerate(self.scores) if i < 10 or now - score["timestamp"] < ONE_WEEK][:25]
    with open(SCORE_FILE, 'w') as scorefile:
      for score in self.scores:
        scorefile.write(str(score) + "\n")

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def get_high_scores(self):
    response = []
    for score in self.scores:
      response.append(score) 
      if len(response) > 4:
        break
    return json.dumps({'scores' : response})

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def get_weekly_scores(self):
    response = []
    now = time.time() 
    for score in self.scores:
      timestamp = score["timestamp"]
      if (now - timestamp) < ONE_WEEK:
        response.append(score) 
        if len(response) > 9:
          break
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
# cherrypy.tree.mount(WebPage(), "/page", {"/" : {"tools.staticdir.on" : True, "tools.staticdir.dir" : "/Prosjekt/python/NorwegianGrammarScrabble/malgramweb", "tools.staticdir.index" : "index.html"}})

cherrypy.engine.start()
cherrypy.engine.block()
