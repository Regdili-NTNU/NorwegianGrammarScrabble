#!/usr/bin/env python
# coding: utf-8

import cherrypy
import parser
import json

class GameServer(object):

  def __init__(self):
    # TODO(eliasaa): Fleire parsarar, avhengig av traad.
    self.parser = parser.ACEParser()
    self.generator = parser.ACEGenerator()

  def analyze(self, sentence, words):
      """Parses the sentence."""
      response = {"original_sentence" : sentence}
      parse_response = self.parser.Parse(sentence.decode("utf-8"))
      errors = self.extract_mal_rules(parse_response.parse_tree)
      response["errors"] = errors

      if errors:
        response["generated_sentence"] = self.generator.Generate(parse_response.mrs)
      # TODO(eliasaa): Vel beste genererte setning
      return json.dumps(response)

  def check_words(self, parse_tree, words):
    """Verifies that only words from the provided input list has been used in
    the parse tree.

    Arguments:
      parse_tree : the parse tree returned by ACE.
      words : the list of permitted words
    
    Returns:
      true if only the permitted words have been used.
    """

    pass

  def extract_mal_rules(self, parse_tree):
    """
      Iterates through the parse tree to figure out which mal rules have been used to generate the
      sentence.

      Arguments:
         parse_tree : the parse tree retuned by ACE.

      Returns:
         a list of the mal-rules that were invoked during creation of the parse tree.
    """
    print parse_tree
    errors = []
    split = parse_tree.split()
    for token in split:
      if token.startswith("mal"):
        errors.append(token)
    return errors

  @cherrypy.expose
  @cherrypy.tools.json_in()
  @cherrypy.tools.json_out()
  def parse(self):
    request = cherrypy.request.json
    sentence = request.get("sentence")
    words = request.get("words")
    response = self.analyze(sentence, words) 
    return response

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def words(self):
    # TODO(eliasaa): Vel ord fra lex
    response = {} 
    response['words'] = ["det", "er", "ikke"]
    for i in xrange(47):
	response['words'].append(str(i))
    return json.dumps(response)

class WebPage(object):
  pass

cherrypy.config.update({'server.socket_port' : 5051, 'server.socket_host' : '0.0.0.0', 'tools.response_headers.on' : True, 'tools.response_headers.headers' : [('Access-Control-Allow-Origin', '*')]})

cherrypy.tree.mount(GameServer(), "/server")
cherrypy.tree.mount(WebPage(), "/page", {"/" : {"tools.staticdir.on" : True, "tools.staticdir.dir" : "/home/regdili/jsonrpcserver/malgramweb", "tools.staticdir.index" : "index.html"}})

cherrypy.engine.start()
cherrypy.engine.block()
