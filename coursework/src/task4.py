# -*- coding: utf-8 -*-

######################################################################
#
# (c) Copyright University of Southampton, 2021
#
# Created By : Stuart E. Middleton
# Created Date : 2021/01/29
# Project : Teaching
#
######################################################################

from __future__ import absolute_import, division, print_function, unicode_literals

import sys, codecs, json, math, time, warnings, re, logging
warnings.simplefilter( action='ignore', category=FutureWarning )

import nltk, numpy, scipy
import pandas as pd
import pycrfsuite

LOG_FORMAT = ('%(levelname) -s %(asctime)s %(message)s')
logger = logging.getLogger( __name__ )
logging.basicConfig( level=logging.INFO, format=LOG_FORMAT )
logger.info('logging started')

from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.tag import pos_tag

def chapTOsen(chapter):
    sentence = sent_tokenize(chapter)
    return sentence

def sent_process(text):
    text = word_tokenize(text)
    text = pos_tag(text)
    return text

def toWord(sent_index, word_indexes, sents):
    phs = []
    for index in word_indexes:
        ph = []
        for i in index:
            ph.append(sents[sent_index][i][0])
        phs.append(ph)
    return phs

def wordsToph(words_list):
    phs = []
    for words in words_list:
        ph = ''
        for w in words:
            ph += w.lower() + ' '
        phs.append(ph.strip())
    return phs

def sp_seqence(num_list):
    slist = []
    a_seq = []
    n = len(num_list)
    for i in range(n):
        if i+1 < n and  num_list[i+1] == (num_list[i] + 1):
            a_seq.append(num_list[i])
        elif num_list[i-1] == (num_list[i] - 1) and i+1 == n:
            a_seq.append(num_list[i])
            slist.append(a_seq)
            a_seq = []
        elif num_list[i-1] == (num_list[i] - 1) and num_list[i+1] != (num_list[i] + 1):
            a_seq.append(num_list[i])
            slist.append(a_seq)
            a_seq = []
        else:
            slist.append([num_list[i]])
    return slist

def get_label_ne(ne_label, data):
    for key in data.keys():
        if isinstance(data[key], dict) and 'type' in data[key] and 'tokens' in data[key]:
            label_type = data[key]['type']
            label = data[key]['tokens']
            for i in label:
                ne_label[i] = label_type
    return ne_label

def atrain_sentence(words, poses, ne_features):
    sentences = []
    for i in range(len(words)):
        sentences.append((words[i], poses[i], ne_features[i]))
    return sentences

def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]

    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'postag': postag,
        'postag[:2]': postag[:2],
    }
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:postag': postag1,
            '-1:postag[:2]': postag1[:2],
        })
    else:
        features['BOS'] = True

    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:postag': postag1,
            '+1:postag[:2]': postag1[:2],
        })
    else:
        features['EOS'] = True

    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, postag, label in sent]

def sent2tokens(sent):
    return [token for token, postag, label in sent]



def get_N(predictions, test_sents):
    require_key = ['DATE', 'CARDINAL', 'ORDINAL', 'NORP','PERSON']
    result = {}
    dates = []
    cardinals = []
    ordinals = []
    norp = []
    person = []

    for i, sentence in enumerate(predictions):
        date_tokens = []
        cardinal_tokens = []
        ordinal_tokens = []
        norp_tokens = []
        person_tokens = []
        for j, word in enumerate(sentence):
            if word in require_key:
                if word == 'DATE':
                    date_tokens.append(j)
                elif word == 'CARDINAL':
                    cardinal_tokens.append(j)
                elif word == 'ORDINAL':
                    ordinal_tokens.append(j)
                elif word == 'NORP':
                    norp_tokens.append(j)
                elif word == 'PERSON':
                    person_tokens.append(j)

        date = wordsToph(toWord(i,sp_seqence(date_tokens),test_sents))
        cardinal = wordsToph(toWord(i,sp_seqence(cardinal_tokens),test_sents))
        ordinal = wordsToph(toWord(i,sp_seqence(ordinal_tokens),test_sents))
        norps = wordsToph(toWord(i,sp_seqence(norp_tokens),test_sents))
        persons = wordsToph(toWord(i,sp_seqence(person_tokens),test_sents))

        dates.extend(date)
        cardinals.extend(cardinal)
        ordinals.extend(ordinal)
        norp.extend(norps)
        person.extend(persons)
        
    
    result['DATE'] = list(set(dates))
    result['CARDINAL'] =list(set(cardinals))
    result['ORDINAL'] = list(set(ordinals))
    result['NORP'] = list(set(norp))
    result['PERSON'] = list(set(person))

    return result


def exec_ner( file_chapter = None, ontonotes_file = None ) :
    ins = []
    train_sets = []
    ontonotes = pd.read_json(ontonotes_file)
    logger.info('ontonotes loaded')
    for index, row in ontonotes.iterrows():  
        for r in row:
            ins.append(r)

    i = 0
    # delete nan
    ins = [i_ for i_ in ins if i_ == i_]
    logger.info('data processed')
    logger.info('data size: {}'.format(len(ins)))
    for data in ins:

        words = []
        poses = []
        ne_labels = []

        words = [w for w in data['tokens']]
        poses = data['pos']
        ne_labels = ['O'] * len(words)
        if 'ne' in data.keys():
            ne_labels = get_label_ne(ne_labels, data['ne'])
            sentence = atrain_sentence(words, poses, ne_labels)
        train_sets.append(sentence)

    X_train = [sent2features(s) for s in train_sets]
    y_train = [sent2labels(s) for s in train_sets]

    trainer = pycrfsuite.Trainer(verbose=False)

    for xseq, yseq in zip(X_train, y_train):
        trainer.append(xseq, yseq)

    trainer.set_params({
        'c1': 1.0,   # coefficient for L1 penalty
        'c2': 1e-3,  # coefficient for L2 penalty
        'max_iterations': 250,  # stop earlier

        # include transitions that are possible, but not observed
        'feature.possible_transitions': True
    })

    trainer.train('conll2002-esp.crfsuite')

    logger.info('trained model')

    tagger = pycrfsuite.Tagger()
    tagger.open('conll2002-esp.crfsuite')

    test_sents = []
    test_file = pd.read_json(file_chapter)
    for index, row in test_file.iterrows():
        chapter = row['content']
        sentences = chapTOsen(chapter)
        for i in range(len(sentences)):
            sentence = sentences[i]
            sent_index = i
            words = [x[0] for x in sent_process(sentence)]
            poses = [x[1] for x in sent_process(sentence)]
            test_sents.append(atrain_sentence(words, poses, ['O']*len(words)))

    X_test = [sent2features(s) for s in test_sents]
    predictions = [tagger.tag(xseq) for xseq in X_test]

    dictNE = get_N(predictions, test_sents)
    writeHandle = codecs.open( 'characters12.txt', 'w', 'utf-8', errors = 'replace' )
    if 'PERSON' in dictNE :
        for strNE in dictNE['PERSON'] :
            writeHandle.write( strNE.strip().lower()+ '\n' )
        writeHandle.close()

if __name__ == '__main__':
	# if len(sys.argv) < 4 :
	# 	raise Exception( 'missing command line args : ' + repr(sys.argv) )
	# ontonotes_file = sys.argv[1]
	# book_file = sys.argv[2]
	# chapter_file = sys.argv[3]

	# logger.info( 'ontonotes = ' + repr(ontonotes_file) )
	# logger.info( 'book = ' + repr(book_file) )
	# logger.info( 'chapter = ' + repr(chapter_file) )

	# # DO NOT CHANGE THE CODE IN THIS FUNCTION

	exec_ner(r'C:\Users\gyh14\nlp\comp3225_example_package\eval_chapter.txt', r'C:\Users\gyh14\nlp\comp3225_example_package\ontonotes_parsed.json' )

