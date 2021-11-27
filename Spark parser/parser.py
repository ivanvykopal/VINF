import re
from io import open
from record import Record
from regex import R_TITLE, R_ALT, R_TYPE, R_EN, R_LANG, R_LANG_TERM

def get_non_types():
    file = open("common_types.txt", 'r', encoding='utf-8')
    lines = set()
    for line in file:
        lines.add(line.strip())
    file.close()
    return lines

def parse_line(line, non_types):
    if -1 != line.find('type.object.name'):
        result = re.search(R_TITLE, line)
        if result:
            return result.group(1), Record(title=result.group(2))

    if -1 != line.find('type.object.type'):
        result = re.search(R_TYPE, line)
        if result:
            string = re.sub(r"[_\.]", " ", result.group(2))
            if string not in non_types:
                return result.group(1), Record(types={string})
            else:
                return None

    if -1 != line.find('common.topic.alias'):
        result = re.search(R_ALT, line)
        if result:
            string = re.search(R_LANG_TERM, result.group(2)).group(1)
            return result.group(1), Record(alternatives={string})

    if -1 != line.find('type.object.name'):
        result = re.search(R_LANG, line)
        if result:
            string = result.group(2)
            if re.search(R_EN, string):
                return None
            string = re.search(R_LANG_TERM, string).group(1)
            return result.group(1), Record(alternatives={string})

    return None
