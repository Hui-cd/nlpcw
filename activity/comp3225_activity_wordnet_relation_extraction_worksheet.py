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
# Created Date : 2022/04/24
# Project : Teaching
# Restriction: Content for internal use at University of Southampton only
#
######################################################################

from __future__ import absolute_import, division, print_function, unicode_literals
import sys, codecs, json, math, time, warnings
warnings.simplefilter( action='ignore', category=FutureWarning )
import logging
import nltk, re

LOG_FORMAT = ('%(levelname) -s %(asctime)s %(message)s')
logger = logging.getLogger( __name__ )
logging.basicConfig( level=logging.INFO, format=LOG_FORMAT )

logger.info('logging started')

### 10 mins ###
# get setup
# py -m pip install nltk
# py
# >> import nltk
# >> nltk.download()
# >> ==> (d)
# >> ==> wordnet
# >> ==> omw
#
# browse the NLTK wordnet and rel extract tutorial docs
# https://www.nltk.org/howto/wordnet.html
# http://www.nltk.org/howto/relextract.html
# https://www.nltk.org/api/nltk.sem.relextract.html
# 
# browse wordnet online
# http://wordnetweb.princeton.edu/perl/webwn
#

if __name__ == '__main__':
	logger.info( 'start wordnet and relational extraction activity' )

	### 15 mins ###
	# look at tutorials around nltk.corpus.wordnet.synsets 
	# https://www.nltk.org/howto/wordnet.html
	# 
	# lemma = word
	# synonym = set of lemma with nearly identical meaning
	# synset = set of synonyms for a specific word sense
	# 
	# (a) use WordNet online to browse the word 'tree'
	# (b) use nltk wordnet to return the 1st synset (word sense) for the word 'tree'
	# (c) use nltk wordnet to return the 2nd synset (word sense) for the word 'tree' and return its two lemma
	# (d) for the previous two lemma return the freq of occurance in WordNet corpus (i.e. count() function)
	# (e) code a function to return the most likely (based on highest occurance freq) synset for the sentence 'that book was great'
	#

	# (a) use WordNet online to browse the word 'tree'
	logger.info( '1st synset for word "book"' )
	# TODO

	# (b) use nltk wordnet to return the 1st synset (word sense) for the word 'tree'
	logger.info( 'lemma for 2nd synset for word "tree"' )
	# TODO

	# (c) use nltk wordnet to return the 2nd synset (word sense) for the word 'tree' and return its two lemma
	logger.info( 'lemma for 2nd synset for word "tree"' )
	# TODO

	# (d) for the previous two lemma return the freq of occurance in WordNet corpus (i.e. count() function)

	strText = 'that book was great'
	logger.info( 'sent = "' + str(strText) + '"' )
	# TODO function get_first_synset
	# TODO print count() freq for lemma

	# (e) code a function to return the most likely (based on highest occurance freq) synset for the sentence 'that book was great'
	logger.info( 'sent = "' + str(strText) + '"' )
	# TODO function get_most_freq_synset
	# TODO print most liekly synset

	### 15 mins ###
	# look at tutorials around nltk.sem.relextract.extract_rels
	# http://www.nltk.org/howto/relextract.html
	# https://www.nltk.org/api/nltk.sem.relextract.html
	# 
	# tuple = (arg, rel, arg)
	# for this NLTK function there are two arguments, but there can be many
	# there can also be argument modifiers (e.g. I am in New York shopping for food ==> arg [I, food] rel [shopping] arg_modifier_location [New York]
	#
	# ieer document headline and text attributes are NLTK Tree objects
	# https://www.nltk.org/_modules/nltk/tree.html
	# 
	# (a) use nltk.sem.relextract.extract_rels to extract 'economist' relation between PER and ORG argument named entity types
	#    role regex = * economist *
	# (b) use nltk.sem.relextract.extract_rels to extract 'in' relation between ORG and LOC argument named entity types
	#    role regex = * in *
	# (c) create a 0-hop and 1-hop knowledge production for 'William Gale' as the subject
	#    target subject = 'William Gale'
	#    0-hop = (William Gale role:economist Brookings Institution)
	#    1-hop = (William Gale, role:economist, Brookings Institution) + (Brookings Institution, loc:in, Washington)
	#

	doc_set = []
	for fileid in nltk.corpus.ieer.fileids() :
		doc_set.extend( nltk.corpus.ieer.parsed_docs( fileid ) )

	logger.info( '1st doc object =' )
	logger.info( repr( type( doc_set[0] ) ) )
	logger.info( ' '.join( doc_set[0].headline.leaves() ) )
	logger.info( ' '.join( doc_set[0].text.leaves() ) )

	# (a) use nltk.sem.relextract.extract_rels to extract 'economist' relation between PER and ORG argument named entity types
	# TODO refine regex role
	# TODO print 1st relation extracted

	# (b) use nltk.sem.relextract.extract_rels to extract 'in' relation between ORG and LOC argument named entity types
	# TODO refine regex role
	# TODO print 1st relation extracted

	# (c) create a 0-hop and 1-hop knowledge production for 'William Gale' as the subject
	# target subject = 'William Gale'
	# 0-hop = (William Gale role:economist Brookings Institution)
	# 1-hop = (William Gale, role:economist, Brookings Institution) + (Brookings Institution, loc:in, Washington)

	target_per = 'William Gale'

	# TODO print 0-hop
	# TODO print 1-hop

