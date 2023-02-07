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

def exec_ner( file_chapter = None, ontonotes_file = None ) :

	# CHANGE CODE BELOW TO TRAIN A NER MODEL AND/OR USE REGEX GENERATE A SET OF BOOK CHARACTERS AND FILTERED SET OF NE TAGS (task 4)

	# Input >> www.gutenberg.org sourced plain text file for a chapter of a book
	# Output >> characters.txt = plain text set of extracted character names. one line per character name.

	# hardcoded output to show exactly what is expected to be serialized (you should change this)
	# only the allowed types for task 4 PERSON will be serialized
	dictNE = {
			"CARDINAL": [
				"two",
				"three",
				"one"
			],
			"ORDINAL": [
				"first"
			],
			"DATE": [
				"saturday",
			],
			"NORP": [
				"indians"
			],
			"PERSON": [
				"creakle",
				"mr. creakle",
				"mrs. creakle",
				"miss creakle"
			]
		}

	# DO NOT CHANGE THE BELOW CODE WHICH WILL SERIALIZE THE ANSWERS FOR THE AUTOMATED TEST HARNESS TO LOAD AND MARK

	# write out all PERSON entries for character list for subtask 4
	writeHandle = codecs.open( 'characters.txt', 'w', 'utf-8', errors = 'replace' )
	if 'PERSON' in dictNE :
		for strNE in dictNE['PERSON'] :
			writeHandle.write( strNE.strip().lower()+ '\n' )
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

	exec_ner( chapter_file, ontonotes_file )

