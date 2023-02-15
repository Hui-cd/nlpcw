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
# copy \\notes.ecs.soton.ac.uk\notes\comp3225\activities\glove.6B.zip to work dir
#
# inspect GloVe embedding weights file glove.6B.300d.txt using a text editor or type/cat on terminal/powershell
#   <word1> <dim_1> ... <dim_300>
#   <word2> <dim_1> ... <dim_300>
#   ...
#   <wordV> <dim_1> ... <dim_300>

# path to work dir with GloVe embeddings unzipped
# download glove.6B.300d from https://nlp.stanford.edu/projects/glove/
work_path = '/projects/datasets/GloVe'

def tokenize_sent( sent ) :
	return nltk.tokenize.word_tokenize( sent )

def cosine_distance( word_list, word_target, embeddings_dict ) :
	# get embeddings for words
	embed_word_list = []
	for word in word_list :
		embed_word_list.append( embeddings_dict[word] )
	embed_target = embeddings_dict[word_target]

	# normalized dot product
	normalized_dot_product = (np.dot(embed_word_list, embed_target) / np.linalg.norm(embed_word_list, axis=1) / np.linalg.norm(embed_target))

	# get indexes for a sorted list
	sorted_word_ids = np.argsort( -normalized_dot_product )

	# return result
	list_scores = []
	for sorted_id in sorted_word_ids :
		word = word_list[sorted_id]
		list_scores.append( (word_list[sorted_id], normalized_dot_product[sorted_id]) )
	return list_scores

if __name__ == '__main__':
	logger.info( 'start GloVe embedding activity' )

	### 10 mins ###
	# load GloVe embedding weights
	# print the word embedding for queen
	# embeddings_dict = { word : [1..300] of float }
	# token_index = [ word1, word2, ... wordN ]
	# token_index_dict = { word : token_index }
	embeddings_dict = {}
	token_index_dict = {}
	token_index = []
	readHandle = codecs.open( work_path + '/glove.6B/glove.6B.300d.txt', 'r', 'utf-8', errors = 'replace' )

	# TODO CODE HERE

	readHandle.close()
	logger.info( 'loaded GloVe embedding weights for ' + str(len(token_index)) + ' words' )
	logger.info( '[queen] >> ' + repr( embeddings_dict['queen'][0:10] ) + '...' )

	### 5 mins ###
	# load GloVe embedding weights (this time keeping an aggregate vector for unk)
	# unk_vec= sum(all_word_vecs) / len(words)
	embeddings_dict = {}
	token_index_dict = {}
	token_index = []
	vect_sum = np.zeros((300,))
	readHandle = codecs.open( work_path + '/glove.6B/glove.6B.300d.txt', 'r', 'utf-8', errors = 'replace' )

	# TODO CODE HERE

	readHandle.close()
	logger.info( 'loaded GloVe embedding weights for ' + str(len(token_index)) + ' words (aggregating for unk)' )

	unk_vec = vect_sum / len(token_index)
	logger.info( '[unk] >> ' + repr( unk_vec[0:10] ) + '...' )

	### 5 mins ###
	# print the similarity between 4 words [dog, kettle, king, princess] and queen
	# print the 5 most similar words to dog
	# explore some other words and look at GloVe embedding similarity
	word_list = [ 'dog', 'kettle', 'king', 'princess' ]
	word_target = 'queen'
	list_sim = cosine_distance( word_list, word_target, embeddings_dict )
	logger.info( '(queen) >> ' + repr( list_sim ) )

	word_target = 'dog'
	list_sim = cosine_distance( token_index, word_target, embeddings_dict )
	logger.info( '(dog) >> ' + repr( list_sim[:5] ) )

	### directed work (solution) - sentence embeddings ###
	# make a sent embedding for 1st sentence in list
	# you will need to tokenize the sentence, then compute word embeddings, then compute sent embedding
	# sent embedding = sum(word_embedding_in_sent) / len(words_in_sent)
	list_sents = [
		'London is the capital and largest city of England and the United Kingdom.',
		'It stands on the River Thames in south-east England at the head of a 50-mile (80 km) estuary down to the North Sea, and has been a major settlement for two millennia.',
		'The City of London, its ancient core and financial centre, was founded by the Romans as Londinium and retains boundaries close to its medieval ones.',
		'Rome is the capital city of Italy.',
		'A banana is an elongated, edible fruit – botanically a berry – produced by several kinds of large herbaceous flowering plants in the genus Musa.'
		]

	sent_embed = np.zeros((300,))

	# TODO CODE HERE

	logger.info( 'sent embedding >> ' + repr( sent_embed[0:10] ) + '...' )

	### directed work (solution) - sentence embeddings ###
	# compare all 5 sentences to the 1st sentence using sent embeddings
	# compute sent embedding for all 5 sentences, then use cosine_distance() to compare them to the first sentence
	# the 1st sentence should be identical (0.999) to itself

	# TODO CODE HERE

	### directed work (no solution) - embedding layers in tensorflow or pytorch ###
	# create an embedding layer (V x 300) initialized using GloVe embeddings
	# create a one-hot input tensor X for a sentence
	# embed X using embedding layer
	# embed a batch of 5 x X using embedding layer 

	# TODO CODE HERE

	logger.info( 'end GloVe embedding activity' )
