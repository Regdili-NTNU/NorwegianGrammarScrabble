import urllib, urllib2
import xml.etree.ElementTree as ET
import json

PARSE_ADDRESS = "http://xregdili.hf.ntnu.no:8081/malgram/rest/parse"
ERROR_ADDRESS = "http://xregdili.hf.ntnu.no:8081/malgram/rest/messages"
GENERATE_ADDRESS = "http://xregdili.hf.ntnu.no:8081/bongram/rest/generate"

# PARSE_ADDRESS = "http://192.168.0.122:8081/MalgramRest/parse"
# ERROR_ADDRESS = "http://192.168.0.122:8081/MalgramRest/messages"
# GENERATE_ADDRESS = "http://192.168.0.122:8081/BongramRest/generate"


def parse_post(statement):
    dict = {"statement" : statement, "client" : "crab", "readings" : 25}
    data = json.dumps(dict)

    req = urllib2.Request(PARSE_ADDRESS, data=data) 
    response = urllib2.urlopen(req).read()
    return response


def error_post(syntax):
    # print 'call_error. syntaxtree: ' + ET.tostring(syntax_tree, encoding='utf-8')
    dict = {"language": "1", "syntax": syntax}
    # data = urllib.urlencode(dict)
    # data = json.dumps(dict).replace('\\"', '"')
    data = json.dumps(dict)
    print 'call_error. data: ' + data
    req = urllib2.Request(ERROR_ADDRESS, data=data) 
    response = urllib2.urlopen(req).read()
    return response

def GetSyntaxTree(parse_xml, i):
    for index, syntax_tree in enumerate(parse_xml.iter("syntaxtree")):
        if i == index:
            return syntax_tree 
        
def GetMrs(parse_xml, i):
    for index, mrs in enumerate(parse_xml.iter("mrs")):
        if i == index:
            return mrs         

def generate_post(mrs, statement):
    dict = {"statement": statement, "mrs": mrs, "client": "scrab"}
    data = json.dumps(dict)
    req = urllib2.Request(GENERATE_ADDRESS, data=data) 
    response = urllib2.urlopen(req).read()
    return response
    
def main():
    statement = "deg smiler"
    xml_str = parse_post(statement)
    parse_xml = ET.fromstring(xml_str)
    syntax_xml = GetSyntaxTree(parse_xml=parse_xml, i=0)
    syntax_str = ET.tostring(syntax_xml, encoding='utf-8') 
    print 'syntax: '+syntax_str
    error_xml = error_post(syntax_str)
    print 'error: '+error_xml

    mrs_xml = GetMrs(parse_xml=parse_xml, i=0)
    mrs_str = ET.tostring(mrs_xml, encoding='utf-8') 
    print 'mrs: '+mrs_str

    generate_str = generate_post(statement=statement, mrs=mrs_str)
    print 'generate: '+generate_str
    
if __name__ == '__main__':
    main()
