from __future__ import absolute_import, division, print_function, unicode_literals

import sys, codecs, json, math, time, warnings, re, logging
warnings.simplefilter( action='ignore', category=FutureWarning )

import nltk, numpy, scipy, sklearn, sklearn_crfsuite, sklearn_crfsuite.metrics

LOG_FORMAT = ('%(levelname) -s %(asctime)s %(message)s')
logger = logging.getLogger( __name__ )
logging.basicConfig( level=logging.INFO, format=LOG_FORMAT )
logger.info('logging started')

import codecs
import re

def exec_regex_questions(file_chapter=None):
    with codecs.open(file_chapter, "r", encoding="utf-8") as file:
        content = file.read()

    cleaned_content = re.sub('\r\n', '\n', content)
    cleaned_content = re.sub('(?<!\n)\n(?!\n)', ' ', cleaned_content)

    pattern = r"(?:(?<=([‘“\"\'\.\?\!]))[ ]*)([A-Za-z][^\?\.!]*\?)"
    found_matches = re.findall(pattern, cleaned_content, flags=re.DOTALL | re.UNICODE)

    additional_matches = []
    for _, match in found_matches:
        additional_matches += re.findall(pattern, match, flags=re.DOTALL | re.UNICODE)

    found_matches += additional_matches

    extracted_questions = set()
    for _, match in found_matches:
        question_text = match.strip().replace('\n', ' ')
        extracted_questions.add(question_text)

    writeHandle = codecs.open( 'questions.txt', 'w', 'utf-8', errors = 'replace' )
    for strQuestion in extracted_questions :
        writeHandle.write( strQuestion + '\n' )
    writeHandle.close()

if __name__ == '__main__' :
    exec_regex_questions( r'comp3225_example_package\eval_chapter.txt' )