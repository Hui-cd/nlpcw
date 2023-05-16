import codecs
import json
import logging

LOG_FORMAT = ('%(levelname) -s %(asctime)s %(message)s')
logger = logging.getLogger( __name__ )
logging.basicConfig( level=logging.INFO, format=LOG_FORMAT )

import re
import json
import codecs


def exec_regex_toc(file_book: str = None):
    text = codecs.open(file_book, "r", encoding="utf-8").read()

    nume = r'\d+'
    roma = r'(?=[MDCLXVI])M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})'
    words = r'(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety(?:[-\s]?(?:one|two|three|four|five|six|seven|eight|nine))?)'
    number_words = r'(?:the\s)?(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth|(?:thir|four|fif|six|seven|eigh|nine)teenth|(?:twen|thir|for|fif|six|seven|eigh|nine)tieth|last)'
    
    enumerators = r'(' + '|'.join([nume, roma, words, number_words]) + ')'
    chapter_pattern = re.compile(r'(?: *\**)chapter +' + enumerators + r'(?:\.+ *|-+ *|—+ *| *)*', re.IGNORECASE)

    lines = text.split('\r\n')

    def extract_title(index):
        title = ""
        while index < len(lines) and lines[index]:
            title += " " + lines[index].strip()
            index += 1
        return title.strip()

    toc = {}
    for i, line in enumerate(lines):
        if i > 0 and not lines[i - 1] and chapter_pattern.match(line):
            match = chapter_pattern.match(line)
            chapter_number = match.group(1)
            title_start = match.span()[1]
            title = line[title_start:].strip() or extract_title(i + 1)
            toc[chapter_number] = title
    writeHandle = codecs.open( 'toc.json', 'w', 'utf-8', errors = 'replace' )
    strJSON = json.dumps( toc, indent=2 )
    writeHandle.write( strJSON + '\n' )
    writeHandle.close()


if __name__ == '__main__':
    exec_regex_toc(r'comp3225_example_package\eval_book.txt')
