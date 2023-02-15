import unicodedata, re, io, time, os, datetime, sys, codecs, math, gc, random, contextlib, itertools, json, string
import numpy as np
import sacrebleu, mosestokenizer

# small library of functions used by this tutorial
import lab_seq2seq_nmt_lib

import logging
import tensorflow as tf
import absl.logging
formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s %(asctime)s] %(message)s')
absl.logging.get_absl_handler().setFormatter(formatter)
absl.logging._warn_preinit_stderr = False
logger = tf.get_logger()
logger.setLevel(logging.INFO)

from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Embedding
from keras.models import load_model
import tensorflow_addons as tfa

# encoder embedding dimension
EMBEDDING_DIM = 256

# encoder LSTM dimension
RNN_UNITS = 1024

# attension layer dimension
DENSE_UNITS = 1024

# dataset parameters
SHUFFLE_BUFFER_SIZE = 10000
MAX_SENT_LENGTH = 20
MAX_SENT_LENGTH_SOURCE = MAX_SENT_LENGTH
MAX_SENT_LENGTH_TARGET = MAX_SENT_LENGTH

# beam search parameters
BEAM_WIDTH = 12
BEAM_LENGTH_NORM_WEIGHT = 1.0

# very short run for debug, will probably provide single wrong word translations (in lab)
BATCH_SIZE = 64
EPOCHS = 10
DEBUG_TRUNC_SENTS = 1000
MAX_VOCAB_SIZE = 1000

# longer run, better accuracy (in lab with a CPU 1.5h, faster with GPU)
#BATCH_SIZE = 256
#EPOCHS = 10
#DEBUG_TRUNC_SENTS = 20000
#MAX_VOCAB_SIZE = 10000

# full run, best accuracy (overnight)
#BATCH_SIZE = 256
#EPOCHS = 100
#DEBUG_TRUNC_SENTS = None
#MAX_VOCAB_SIZE = 10000