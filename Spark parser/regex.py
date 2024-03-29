R_TITLE = r'<http:\/\/rdf\.freebase\.com\/ns\/([a-zA-Z]\.[_a-zA-Z0-9]+)>\s+<.*type\.object\.name>\s+\"(.*)\"@en'
R_TYPE = r'<http:\/\/rdf\.freebase\.com\/ns\/([a-zA-Z]\.[_a-zA-Z0-9]+)>\s+<.*type\.object\.type\>\s<.*ns\/(.*)>'
R_ALT = r'<http:\/\/rdf\.freebase\.com\/ns\/([a-zA-Z]\.[_a-zA-Z0-9]+)>\s+<.*common\.topic\.alias>\s(\".*)\s\.'
R_LANG = r'<http:\/\/rdf\.freebase\.com\/ns\/([a-zA-Z]\.[_a-zA-Z0-9]+)>\s+<.*type\.object\.name>\s(\".*)\s\.'
R_EN = r'\".*\"@en'
R_LANG_TERM = r'"(.*)"@.+'
R_FILE_TITLE = r'title:\s+(.*)'
R_FILE_TYPE = r'type:\s+(.*)'
R_FILE_ALT = r'alternative:\s+(.*)'
R_DIGIT_WORD = r'[\-\,\.\&\#\?\!\;\_\(\)\/\\\+\%\?\$\'\*\<\>\" \t\:\xa0]'
R_MAX_COUNT = r'(.*) -n\s+([\d]+)'
