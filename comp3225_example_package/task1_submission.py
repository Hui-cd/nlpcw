# !/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################
#
# (c) Copyright University of Southampton, 2021
#
# Copyright in this software belongs to University of Southampton,
# Highfield, University Road, Southampton SO17 1BJ
#
# Created By : Stuart E. Middleton
# Created Date : 2021/01/29
# Project : Teaching
#
######################################################################

from __future__ import absolute_import, division, print_function, unicode_literals

import sys, codecs, json, math, time, warnings, re, logging
warnings.simplefilter( action='ignore', category=FutureWarning )

import nltk, numpy, scipy, sklearn, sklearn_crfsuite, sklearn_crfsuite.metrics

LOG_FORMAT = ('%(levelname) -s %(asctime)s %(message)s')
logger = logging.getLogger( __name__ )
logging.basicConfig( level=logging.INFO, format=LOG_FORMAT )
logger.info('logging started')



def exec_regex_toc(file_book=None):
    # Read the book content
    text = codecs.open(file_book, "r", encoding="utf-8").read()

    # Define regex patterns
    patterns = [
        r"^(?:CHAPTER|STAVE|Chapter|Book|BOOK|PART|Part|VOLUME)\s(\w+)\.?(?:\r\n(?:\r\n)?|\s*)((.*\s{2})+)",
        r"^(\d+)\.\s+(_.*?\?*_)\s*$",
        r"^([IVXLCDM]+)\s+(.*)"
    ]

    # Iterate through patterns and find matches
    for pattern in patterns:
        matches = re.findall(pattern, text, re.MULTILINE)
        if matches:
            break

    # Process matches
    dictTOC = {}
    for match in matches:
        chapterTitle = match[1].replace("\r\n", " ").replace("\r", "").rstrip()
        dictTOC[match[0]] = chapterTitle
    
    writeHandle = codecs.open( 'toc.json', 'w', 'utf-8', errors = 'replace' )
    strJSON = json.dumps( dictTOC, indent=2 )
    writeHandle.write( strJSON + '\n' )
    writeHandle.close()

if __name__ == '__main__':
	if len(sys.argv) < 4 :
		raise Exception( 'missing command line args : ' + repr(sys.argv) )
	ontonotes_file = sys.argv[1]
	book_file = sys.argv[2]
	chapter_file = sys.argv[3]

	logger.info( 'ontonotes = ' + repr(ontonotes_file) )
	logger.info( 'book = ' + repr(book_file) )
	logger.info( 'chapter = ' + repr(chapter_file) )

	# DO NOT CHANGE THE CODE IN THIS FUNCTION

	exec_regex_toc( book_file )