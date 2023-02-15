import sys, codecs, json, math, time, warnings
warnings.simplefilter( action='ignore', category=FutureWarning )

import nltk, scipy, sklearn, sklearn_crfsuite, sklearn_crfsuite.metrics, eli5
from sklearn.metrics import make_scorer
from collections import Counter
import matplotlib.pyplot as plt
from IPython.display import display    

import logging
import tensorflow as tf
import absl.logging
formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s %(asctime)s] %(message)s')
absl.logging.get_absl_handler().setFormatter(formatter)
absl.logging._warn_preinit_stderr = False
logger = tf.get_logger()
logger.setLevel(logging.INFO)

# number of CRF iterations to train for. Using 150 will provide much better results, but take a lot longer to compute.
max_iter = 20

# number of ontonotes training files to load. Using a value of None will load the entire dataset, taking the longest
# to train but providing a much larger sentence corpus to train over and thus is able to learn a larger vocabulary.
max_files = 50

# set of NE label types to display in results. this is simply to limit the amount of logging that is perfoemed later
# when displaying details such as state transitions and top N features per state.
display_label_subset = [ 'B-DATE', 'I-DATE', 'B-GPE', 'I-GPE', 'B-PERSON', 'I-PERSON', 'O' ]

def create_dataset( max_files = None ) :
	dataset_file = '..\corpus\ontonotes_parsed.json'
    
	# load parsed ontonotes dataset
	readHandle = codecs.open( dataset_file, 'r', 'utf-8', errors = 'replace' )
	str_json = readHandle.read()
	readHandle.close()
	dict_ontonotes = json.loads( str_json )

	# make a training and test split
	list_files = list( dict_ontonotes.keys() )
	if len(list_files) > max_files :
		list_files = list_files[ :max_files ]
	nSplit = math.floor( len(list_files)*0.9 )
	list_train_files = list_files[ : nSplit ]
	list_test_files = list_files[ nSplit : ]

	# sent = (tokens, pos, IOB_label)
	list_train = []
	for str_file in list_train_files :
		for str_sent_index in dict_ontonotes[str_file] :
			# ignore sents with non-PENN POS tags
			if 'XX' in dict_ontonotes[str_file][str_sent_index]['pos'] :
				continue
			if 'VERB' in dict_ontonotes[str_file][str_sent_index]['pos'] :
				continue

			list_entry = []

			# compute IOB tags for named entities (if any)
			ne_type_last = None
			for nTokenIndex in range(len(dict_ontonotes[str_file][str_sent_index]['tokens'])) :
				strToken = dict_ontonotes[str_file][str_sent_index]['tokens'][nTokenIndex]
				strPOS = dict_ontonotes[str_file][str_sent_index]['pos'][nTokenIndex]
				ne_type = None
				if 'ne' in dict_ontonotes[str_file][str_sent_index] :
					dict_ne = dict_ontonotes[str_file][str_sent_index]['ne']
					if not 'parse_error' in dict_ne :
						for str_NEIndex in dict_ne :
							if nTokenIndex in dict_ne[str_NEIndex]['tokens'] :
								ne_type = dict_ne[str_NEIndex]['type']
								break
				if ne_type != None :
					if ne_type == ne_type_last :
						strIOB = 'I-' + ne_type
					else :
						strIOB = 'B-' + ne_type
				else :
					strIOB = 'O'
				ne_type_last = ne_type

				list_entry.append( ( strToken, strPOS, strIOB ) )

			list_train.append( list_entry )

	list_test = []
	for str_file in list_test_files :
		for str_sent_index in dict_ontonotes[str_file] :
			# ignore sents with non-PENN POS tags
			if 'XX' in dict_ontonotes[str_file][str_sent_index]['pos'] :
				continue
			if 'VERB' in dict_ontonotes[str_file][str_sent_index]['pos'] :
				continue

			list_entry = []

			# compute IOB tags for named entities (if any)
			ne_type_last = None
			for nTokenIndex in range(len(dict_ontonotes[str_file][str_sent_index]['tokens'])) :
				strToken = dict_ontonotes[str_file][str_sent_index]['tokens'][nTokenIndex]
				strPOS = dict_ontonotes[str_file][str_sent_index]['pos'][nTokenIndex]
				ne_type = None
				if 'ne' in dict_ontonotes[str_file][str_sent_index] :
					dict_ne = dict_ontonotes[str_file][str_sent_index]['ne']
					if not 'parse_error' in dict_ne :
						for str_NEIndex in dict_ne :
							if nTokenIndex in dict_ne[str_NEIndex]['tokens'] :
								ne_type = dict_ne[str_NEIndex]['type']
								break
				if ne_type != None :
					if ne_type == ne_type_last :
						strIOB = 'I-' + ne_type
					else :
						strIOB = 'B-' + ne_type
				else :
					strIOB = 'O'
				ne_type_last = ne_type

				list_entry.append( ( strToken, strPOS, strIOB ) )

			list_test.append( list_entry )

	return list_train, list_test