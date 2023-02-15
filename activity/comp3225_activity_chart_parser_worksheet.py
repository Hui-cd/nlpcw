# !/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################
#
# (c) Copyright University of Southampton, 2022
#
# Copyright in this software belongs to University of Southampton,
# Highfield, University Road, Southampton SO17 1BJ
#
# Created By : Stuart E. Middleton
# Created Date : 2022/03/07
# Project : Teaching
# Restriction: Content for internal use at University of Southampton only
#
######################################################################

from __future__ import absolute_import, division, print_function, unicode_literals
import sys, codecs, json, math, time, warnings
warnings.simplefilter( action='ignore', category=FutureWarning )
import nltk
import numpy as np
import logging

LOG_FORMAT = ('%(levelname) -s %(asctime)s %(message)s')
logger = logging.getLogger( __name__ )
logging.basicConfig( level=logging.INFO, format=LOG_FORMAT )

logger.info('logging started')

### 10 mins ###
# get setup
# py -m pip install numpy
# py -m pip install nltk
# py
# >> import nltk
# >> nltk.download()
# >>   ==> (d) all OR
# >>   ==> stopwords
# >>   ==> names
# >>   ==> wordnet
# >>   ==> omw
# >> quit()
#
# read nltk tutorial docs
# https://www.nltk.org/book_1ed/ch08-extras.html
# http://www.nltk.org/howto/parse.html
# https://www.nltk.org/_modules/nltk/parse/chart.html
#

if __name__ == '__main__':
	logger.info( 'start chart parser activity' )

	### 10 mins ###
	# create a CFG for the sentence "I shot some dinosaurs"
	# use nltk.pos_tag to print POS tags for words
	# use the nltk.CFG model to create a grammar to parse this sentence
	#   S = sentence containing 4 tokens which can be nouns or verbs
	#   N = noun
	#   V = verb
	#   DET = determiner
	#   PRO = pronoun
	#
	# print the resulting chart
	#

	sent = ['I', 'shot', 'some', 'dinosaurs']

	logger.info( 'sent = ' + repr( sent ) )
	logger.info( 'POS = ' + repr( nltk.pos_tag( sent ) ) )

	# TODO CODE HERE (to make chart object)

	for tree in chart :
		logger.info( str(tree) )


	### 10 mins ###
	# visualize your chart using ChartParserApp and compare parsing strategies
	# which one is more efficient ?
	#
	# nltk.app.chartparser_app.ChartParserApp( grammar = dino_grammar, tokens = sent ).mainloop()
	#
	# TD_STRATEGY >> top down
	# BU_STRATEGY >> bottom up
	# BU_LC_STRATEGY >> bottom up left corner
	# LC_STRATEGY >> left corner
	#
	# try it without the app also using the below command
	# parser = nltk.parse.chart.ChartParser( grammar = dino_grammar, strategy = strat, trace = None )
	#

	nltk.app.chartparser_app.ChartParserApp( grammar = dino_grammar, tokens = sent ).mainloop()

	# TODO CODE HERE (output chart results for different parser strategies without app)

	### 20 mins ###
	# dynamically create a grammar using the POS tagger to inject the literal terms
	# test on sentence
	# "I shot some dinosaurs before breakfast"
	#
	#   S = NOUN_P VERB_P NOUN_P
	#   NOUN_P = N NOUN_P | N | DET NOUN_P | PRO | NOUN_P PREP NOUN_P
	#   VERB_P = V VERB_P | V | VERB_P NOUN_P
	#
	#   PREP = any word with POS tag = IN | TO
	#   PRO = any word with POS tag = PRP | PRP$
	#   DET = any word with POS tag = DT
	#   N = any word with POS tag = NN | NP | NNS | NNPS
	#   V = any word with POS tag = VBP | VBD | VBG | VBN | VBZ | VB
	# 

	sent = ['I', 'shot', 'some', 'dinosaurs', 'before', 'breakfast']
	list_pos = nltk.pos_tag( sent )

	logger.info( 'sent = ' + repr( sent ) )
	logger.info( 'POS = ' + repr( list_pos ) )

	dynamic_grammar = """
S -> NOUN_P VERB_P
NOUN_P -> N NOUN_P | N | NOUN_P PREP NOUN_P | DET NOUN_P | PRO
VERB_P -> V VERB_P | V NOUN_P
PREP -> IN | TO
N -> NN | NP | NNS | NNPS
V -> VBP | VBD | VBG | VBN | VBZ | VB
DET -> DT
PRO -> PRP | PRP_S
"""

	# TODO CODE HERE (POS tag sentence and append lexical productions to dynamic_grammar)

	dino_grammar = nltk.CFG.fromstring( dynamic_grammar )
	nltk.app.chartparser_app.ChartParserApp( grammar = dino_grammar, tokens = sent ).mainloop()

	### directed work (solution) - extract collapsed NOUN_P and VERB_P branches ###
	# Extract from your chart the text of the NOUN_P and VERB_P branches
	# make sure you collapse the branch to capture all the tokens

	# TODO CODE HERE

	### directed work (no solution) - explore scalability of CFG ###
	# CFG do not scale well. However, they are useful for controlled dialogue, such as instructions for a robot or chatbot. 
	# Text vocabulary scaling - try some other words in the sentence using a sentence with similar clause structure, how does it perform?
	# Text structure scaling - try to change CFG to work for other clause types. How easy is it? could you automate it? can it scale to arbitary language grammar?

	# TODO CODE HERE
