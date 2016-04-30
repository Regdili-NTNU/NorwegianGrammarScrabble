"""
  Reads the files in the translation directory and creates the translation
  service JavaScript code.
"""
import os

# (string_name) => (language_name) => actual_string
translations = {}

# Read inputs
for filename in os.listdir("malgramweb/translations"):
  lang_to_string = {}
  with open("malgramweb/translations/" + filename) as tfile:
    for line in tfile:
      line = line.strip()
      # Skip comments
      if line[0] == "#":
        continue
      split = line.split("\t")
      # Skip malformed lines with a warning
      if len(split) != 2:
        print "Skipping malformed line: " + line
      
      lang_to_string[split[0]] = split[1]
  translations[filename] = lang_to_string


# Write service file
def create_single_rule(string_name, lang_to_string_map):
  rstring = """\tthis.%s = function() {
\t\tvar language = this.getLanguage();\n""" % string_name
  for lang, string in lang_to_string_map.iteritems():
    if lang == "en":
      continue
    rstring += """\t\tif (language == '%s') {
\t\t\treturn '%s';
\t\t}\n""" % (lang, string)
  rstring += """\t\treturn '%s';
\t}\n""" % lang_to_string_map["en"] 
  return rstring


with open('malgramweb/src/translationService.js', 'w') as outfile:
  outfile.write("""app.service('translationService', function($window) {
\tthis.getLanguage = function() {
\t\tvar languageString = $window.navigator.language;
\t\tif (languageString.indexOf('no') >= 0) {
\t\t\treturn "no";
\t\t}
\t\tif (languageString.indexOf('pl') >= 0) {
\t\t\treturn "pl";
\t\t}
\t\tif (languageString.indexOf('it') >= 0) {
\t\t\treturn "it";
\t\t}
\t\tif (languageString.indexOf('de') >= 0) {
\t\t\treturn "de";
\t\t}
\t\tif (languageString.indexOf('zh') >= 0) {
\t\t\treturn "zh";
\t\t}
\t\tif (languageString.indexOf('ar') >= 0) {
\t\t\treturn "ar";
\t\t}
\t\tif (languageString.indexOf('bg') >= 0) {
\t\t\treturn "bg";
\t\t}
\t\treturn "en";
\t};
\t
\tthis.getRtl = function() {
\t\t return this.getLanguage() == "ar" ? "rtl" : "ltr";
\t};
\tthis.start_new_game_string_no = function() {
\t\t return "Start ny runde (Norsk)";
\t};
\tthis.start_new_game_string_en = function() {
\t\t return "Start new game (english)";
\t};
\tthis.start_new_game_string_pl = function() {
\t\t return "Start new game (polish)";
\t};
\tthis.start_new_game_string_it = function() {
\t\t return "Start new game (italiano)";
\t};
\tthis.start_new_game_string_de = function() {
\t\t return "Neues Spiel (Deutsch)";
\t};
\tthis.start_new_game_string_zh = function() {
\t\t return "Start new game (zhongwen)";
\t};
\tthis.start_new_game_string_ar = function() {
\t\t return "Start new game (arabic)";
\t};
\tthis.start_new_game_string_bg = function() {
\t\t return "Start new game (bulgarian)";
\t};
""")
  for string_name, lang_string_map in translations.iteritems():
    outfile.write("\n" + create_single_rule(string_name, lang_string_map))
  outfile.write("});")
