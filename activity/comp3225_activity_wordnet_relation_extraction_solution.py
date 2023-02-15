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
	logger.info( repr( nltk.corpus.wordnet.synsets( 'book' )[0] ) )

	# (b) use nltk wordnet to return the 1st synset (word sense) for the word 'tree'
	logger.info( 'lemma for 2nd synset for word "tree"' )
	logger.info( repr( nltk.corpus.wordnet.synsets( 'book' )[1].lemmas() ) )

	# (c) use nltk wordnet to return the 2nd synset (word sense) for the word 'tree' and return its two lemma
	logger.info( 'lemma for 2nd synset for word "tree"' )
	syn = nltk.corpus.wordnet.synsets( 'book' )[1]
	for lemma in syn.lemmas() :
		logger.info( repr( lemma ) + ' = ' + str(lemma.count()) )

	# (d) for the previous two lemma return the freq of occurance in WordNet corpus (i.e. count() function)
	def get_first_synset( sent ) :
		list_result = []
		list_pos = nltk.pos_tag( sent.split(' ') )
		for (str_lemma,pos_tag) in list_pos :
			if pos_tag.startswith('N') :
				pos_flag = nltk.corpus.wordnet.NOUN
			elif pos_tag.startswith('V') :
				pos_flag = nltk.corpus.wordnet.VERB
			elif pos_tag.startswith('J') :
				pos_flag = nltk.corpus.wordnet.ADJ
			elif pos_tag.startswith('R') :
				pos_flag = nltk.corpus.wordnet.ADV
			else :
				pos_flag = None

			list_synsets = nltk.corpus.wordnet.synsets( str_lemma, pos_flag )
			if len(list_synsets) > 0 :
				list_result.append( list_synsets[0] )

		return list_result

	strText = 'that book was great'
	logger.info( 'sent = "' + str(strText) + '"' )
	logger.info( 'wordnet 1st synsets = ' + repr( get_first_synset( strText ) ) )

	# (e) code a function to return the most likely (based on highest occurance freq) synset for the sentence 'that book was great'
	def get_common_synset( sent ) :
		list_result = []
		list_pos = nltk.pos_tag( sent.split(' ') )
		for (str_lemma,pos_tag) in list_pos :
			if pos_tag.startswith('N') :
				pos_flag = nltk.corpus.wordnet.NOUN
			elif pos_tag.startswith('V') :
				pos_flag = nltk.corpus.wordnet.VERB
			elif pos_tag.startswith('J') :
				pos_flag = nltk.corpus.wordnet.ADJ
			elif pos_tag.startswith('R') :
				pos_flag = nltk.corpus.wordnet.ADV
			else :
				pos_flag = None

			list_synsets = nltk.corpus.wordnet.synsets( str_lemma, pos_flag )

			nHighestFreq = 0
			best_syn = None
			for entry_syn in list_synsets :
				for entry_lemma in entry_syn.lemmas() :
					if nHighestFreq < entry_lemma.count() :
						nHighestFreq = entry_lemma.count()
						best_syn = entry_syn
			list_result.append( best_syn )

		return list_result

	logger.info( 'sent = "' + str(strText) + '"' )
	logger.info( 'wordnet best synsets = ' + repr( get_first_synset( strText ) ) )

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
	regex_role = re.compile( r'(.* )economist(.* )' )

	list1 = []
	for doc in doc_set :
		for rel in nltk.sem.relextract.extract_rels('PER', 'ORG', doc, corpus='ieer', pattern=regex_role) :
			list1.append( rel )

	logger.info( '1st relation for "economist" rel pattern' )
	logger.info( 'subjtext = ' + list1[0]['subjtext'] )
	logger.info( 'subjclass = ' + list1[0]['subjclass'] )
	logger.info( 'objtext = ' + list1[0]['objtext'] )
	logger.info( 'objclass = ' + list1[0]['objclass'] )
	logger.info( 'rel filler = ' + list1[0]['filler'] )

	# (b) use nltk.sem.relextract.extract_rels to extract 'in' relation between ORG and LOC argument named entity types
	regex_in = re.compile( r'(.* )in' )

	list2 = []
	for doc in doc_set :
		for rel in nltk.sem.relextract.extract_rels('ORG', 'LOC', doc, corpus='ieer', pattern=regex_in) :
			list2.append( rel )

	logger.info( '1st relation for "in" rel pattern' )
	logger.info( 'subjtext = ' + list2[0]['subjtext'] )
	logger.info( 'subjclass = ' + list2[0]['subjclass'] )
	logger.info( 'objtext = ' + list2[0]['objtext'] )
	logger.info( 'objclass = ' + list2[0]['objclass'] )
	logger.info( 'rel filler = ' + list2[0]['filler'] )

	# (c) create a 0-hop and 1-hop knowledge production for 'William Gale' as the subject
	# target subject = 'William Gale'
	# 0-hop = (William Gale role:economist Brookings Institution)
	# 1-hop = (William Gale, role:economist, Brookings Institution) + (Brookings Institution, loc:in, Washington)

	target_per = 'William Gale'

	list_kb = []
	for rel in list1 :
		if rel ['subjtext'] == target_per :
			list_kb.append( ( rel ['subjtext'], 'role:economist', rel['objtext'] ) )

	list_orgs = []
	for tuple_zero_hop in list_kb :
		list_orgs.append( tuple_zero_hop[2] )

	for rel in list2 :
		for org in list_orgs :
			if rel ['subjtext'] == org :
				list_kb.append( ( org, 'loc:in', rel['objtext'] ) )

	logger.info( repr( list_kb ) )
