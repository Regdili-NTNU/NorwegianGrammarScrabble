import subprocess
import pexpect
import re

class ACEParser:
  """Wrapper around a parser instance of ACE"""
  
  def __init__(self):
    self.ace_process = pexpect.spawnu("../wrapperscripts/mal_p_prod")

  def Parse(self, sentence):
    """Passes on a sentence to the ACE instane for parsing.
    
    Arguments:
      sentence : a unicode string to be parsed.

    Returns:
      a ParseResponse object containing the mrs and the parse tree.
    """
    self.ace_process.sendline(sentence) 
    self.ace_process.expect(u"\r\n")
    while self.ace_process.before:
      if IsMainContentLine(self.ace_process.before):
	parse_response = ExtractParseResponse(self.ace_process.before)
      self.ace_process.expect(u"\r\n")
    # ACE always prints an extra blank line.
    self.ace_process.expect(u"\r\n")
    return parse_response

def IsMainContentLine(line):
  return line[0] == '['

def ExtractParseResponse(line):
  mrs, tree = line.split(" ; ")
  response = ParseResponse(mrs=mrs, parse_tree=tree)
  return response

class ParseResponse:
  """Data class to hold the response for a parse."""

  def __init__(self, mrs=None, parse_tree=None):
    self.mrs = mrs
    self.parse_tree = parse_tree

class ACEGenerator:
  """Wrapper around a generator instance of ACE"""
  
  def __init__(self):
    self.ace_process = pexpect.spawnu("../wrapperscripts/bon_g_prod")

  def Generate(self, mrs):
    """Passes on an MRS to the ACE instance for generation.

      Arguments:
        mrs : the MRS to generate from.

      Returns:
        a unicode string containing the generated sentence.
    """
    self.ace_process.sendline(mrs) 
    response_lines = []
    self.ace_process.expect(u"\r\n")
    while not IsLastGeneratorLine(self.ace_process.before):
      response_lines.append(self.ace_process.before)
      self.ace_process.expect(u"\r\n")
    # First line is always the request MRS
    return response_lines[1:]

def IsLastGeneratorLine(line):
  return line[0:4] == "NOTE"
