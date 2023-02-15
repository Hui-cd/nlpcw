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
# Created Date : 2022/03/21
# Project : Teaching
# Restriction: Content for internal use at University of Southampton only
#
######################################################################

from __future__ import absolute_import, division, print_function, unicode_literals
import sys, codecs, json, math, time, warnings
warnings.simplefilter( action='ignore', category=FutureWarning )
import logging
import stanza
from stanza.models.common.doc import Document

LOG_FORMAT = ('%(levelname) -s %(asctime)s %(message)s')
logger = logging.getLogger( __name__ )
logging.basicConfig( level=logging.INFO, format=LOG_FORMAT )

logger.info('logging started')

### 10 mins ###
# get setup
# py -m pip install stanza
# mkdir /stanza
# py
# >> imporrt stanza
# >> stanza.download( lang='en', processors='tokenize,mwt,pos,lemma,depparse', model_dir='/stanza' )
#
# browse the stanza tutorial docs
# https://stanfordnlp.github.io/stanza/installation_usage.html
# https://stanfordnlp.github.io/stanza/depparse.html
#

if __name__ == '__main__':
	logger.info( 'start stanza dep parser activity' )

	### 10 mins ###
	# use the stanza pipeline to parse the string below and return a stanza doc object
	# use english language 'en' and processors 'tokenize,mwt,pos,lemma,depparse'
	# pipeline flags
	#  tokenize = tokenize words
	#  mwt = multi word tokens
	#  pos = parts of speech tags
	#  lemma = identify lemma
	#  depparse = dependancy parse
	#
	# parser objects
	#  doc = document object returned by parser
	#  doc.sentences = iterator for sent's in parser output
	#  sent.words = iterator for word's in a sent
	#  word.text = token text of word
	#  word.upos = universal POS tag for word
	#  word.deprel = dep parse relation for word
	#

	str_text = 'Author developed approaches are based on (a) entity matching using an OpenStreetMap (OSM) database, and (b) a language model using a combination of a large social media tag dataset and multiple gazetteers.'

	nlp = stanza.Pipeline( lang='en', processors='tokenize,mwt,pos,lemma,depparse', dir='/stanza' )
	doc = nlp( str_text )

	# print the tokens and POS tags for the first sentence
	logger.info( '\n\nsent = ' + str_text )
	for sent in doc.sentences :
		for word in sent.words :
			logger.info( '\t' + word.text + '\t POS = ' + word.upos + '\t dep = ' + word.deprel )
		break

	### 15 mins ###
	# write a function to print all the token indexes for the dep graph branch under a given head token index
	#   word.id = index of token in dep tree
	#   word.head = index of parent token in dep tree
	#
	# print the token indexes under branch for token index 11 = word 'using'

	def collapse_tree( sent,index ) :
		list_result = []
		head_id = None
		for word in sent.words :
			if word.head == index :
				list_result.extend( collapse_tree( sent, word.id ) )
			elif word.id == index :
				head_id = word.id
		list_result.insert( 0,head_id )
		return list_result

	logger.info( '\n\nsent = ' + str_text )
	for sent in doc.sentences :
		logger.info( 'collapsed dep graph for verb "' + sent.words[11].text + '" = ' + repr(collapse_tree( sent, sent.words[11].id )) )
		break

	### 10 mins ###
	# write a function to print the words of a dep graph branch under a head node
	# make sure the words are printed in the order they appear in the original sentence (so it makes sense)
	#

	def print_span( sent, list_ids ) :
		sorted_ids = sorted( list_ids )
		list_result = []
		for index in sorted_ids :
			list_result.append( sent.words[index-1].text )
		return ' '.join( list_result )

	logger.info( '\n\nsent = ' + str_text )
	for sent in doc.sentences :
		logger.info( 'collapsed dep graph for verb "' + sent.words[11].text + '" = ' + print_span( sent, collapse_tree( sent, sent.words[11].id ) ) )
		break

	### directed work (solution) - print for all verbs in sentence the collapsed dep graph ###
	# this is how you can extract clausal stuctures from a dep graph
	# clausal structures can be mapped to (subj,pred,obj) type knowledge graphs, allowing a pathway to information extraction of useful knowledge from documents
	#
	logger.info( '\n\nsent = ' + str_text )
	for sent in doc.sentences :
		for word in sent.words :
			if word.upos == 'VERB' :
				logger.info( '\tVerb = ' + word.text + '; Clause = ' + print_span( sent,collapse_tree( sent, word.id ) )  )

