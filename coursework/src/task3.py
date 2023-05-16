import codecs
import json
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.tag import pos_tag
import pandas as pd
import sklearn_crfsuite


def chapter2sentences(chapter):
    sentences = sent_tokenize(chapter)
    return sentences

def sentence_preprocess(text):
    text = word_tokenize(text)
    text = pos_tag(text)
    return text
def index2word(sent_index, word_indexes, sents):
    phrases = []
    for index in word_indexes:
        phrase = []
        for i in index:
            phrase.append(sents[sent_index][i][0])
        phrases.append(phrase)
    return phrases

def words2phrase(words_list):
    phrases = []
    for words in words_list:
        phrase = ''
        for w in words:
            phrase += w.lower() + ' '
        phrases.append(phrase.strip())
    return phrases

def split_seq(num_list):
    seq_list = []
    a_seq = []
    for i in range(len(num_list)):
        if i+1 < len(num_list) and  num_list[i+1] == (num_list[i] + 1):
            a_seq.append(num_list[i])
        elif num_list[i-1] == (num_list[i] - 1) and i+1 == len(num_list):
            a_seq.append(num_list[i])
            seq_list.append(a_seq)
            a_seq = []
        elif num_list[i-1] == (num_list[i] - 1) and num_list[i+1] != (num_list[i] + 1):
            a_seq.append(num_list[i])
            seq_list.append(a_seq)
            a_seq = []
        else:
            seq_list.append([num_list[i]])
    return seq_list

def get_ne_feature(ne_features, ne_json):
    for key in ne_json.keys():
        # 确保 ne_json[key] 是字典类型
        if isinstance(ne_json[key], dict) and 'type' in ne_json[key] and 'tokens' in ne_json[key]:
            feature_type = ne_json[key]['type']
            addes = ne_json[key]['tokens']
            for i in addes:
                ne_features[i] = feature_type
    return ne_features

def assemble_train_sentence(words, poses, ne_features):
    train_sentence = []
    for i in range(len(words)):
        train_sentence.append((words[i], poses[i], ne_features[i]))
    return train_sentence


# build feature
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

def get_nes(predictions, test_sents):
    required_nes = ['DATE', 'CARDINAL', 'ORDINAL', 'NORP','PERSON']
    ne_dict = {}
    dates = []
    cardinals = []
    ordinals = []
    norp = []
    person = []

    for i, sentence in enumerate(predictions):
        sen_date_tokens = []
        sen_cardinal_tokens = []
        sen_ordinal_tokens = []
        sen_norp_tokens = []
        sen_person_tokens = []
        for j, word in enumerate(sentence):
            if word in required_nes:
                if word == 'DATE':
                    sen_date_tokens.append(j)
                elif word == 'CARDINAL':
                    sen_cardinal_tokens.append(j)
                elif word == 'ORDINAL':
                    sen_ordinal_tokens.append(j)
                elif word == 'NORP':
                    sen_norp_tokens.append(j)
                elif word == 'PERSON':
                    sen_person_tokens.append(j)

        sen_date_tokens = words2phrase(index2word(i,split_seq(sen_date_tokens),test_sents))
        sen_cardinal_tokens = words2phrase(index2word(i,split_seq(sen_cardinal_tokens),test_sents))
        sen_ordinal_tokens = words2phrase(index2word(i,split_seq(sen_ordinal_tokens),test_sents))
        sen_norp_tokens = words2phrase(index2word(i,split_seq(sen_norp_tokens),test_sents))
        sen_person_tokens = words2phrase(index2word(1,split_seq(sen_person_tokens),test_sents))
        
        dates.extend(sen_date_tokens)
        cardinals.extend(sen_cardinal_tokens)
        ordinals.extend(sen_ordinal_tokens)
        norp.extend(sen_norp_tokens)
        person.extend(sen_person_tokens)
    
    ne_dict['DATE'] = list(set(dates))
    ne_dict['CARDINAL'] =list(set(cardinals))
    ne_dict['ORDINAL'] = list(set(ordinals))
    ne_dict['NORP'] = list(set(norp))
    ne_dict['PERSON'] = list(set(person))

    return ne_dict

def exec_ner( file_chapter = None, ontonotes_file = None ) :

    instances = []
    train_sents = []
    ontonote = pd.read_json(ontonotes_file)

    for index, row in ontonote.iterrows():  
        for r in row:
            instances.append(r)

    print(len(instances))
    i = 0
    # delete nan
    instances = [i_ for i_ in instances if i_ == i_]

    for instance in instances:
        # i += 1
        # print(i)
        # print(instance)
        words = []
        poses = []
        ne_labels = []

        words = [w for w in instance['tokens']]
        poses = instance['pos']
        ne_labels = ['O'] * len(words)
        if 'ne' in instance.keys():
            ne_labels = get_ne_feature(ne_labels, instance['ne'])
            train_sentence = assemble_train_sentence(words, poses, ne_labels)
        train_sents.append(train_sentence)

    print(len(train_sents))
    X_train = [sent2features(s) for s in train_sents]
    y_train = [sent2labels(s) for s in train_sents]
    print('training')
    crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.1,
    c2=0.1,
    max_iterations=100,
    all_possible_transitions=True
)
    try:
        crf.fit(X_train, y_train)
    except AttributeError:
        pass
    print('testing')
    test_chapter = open(file_chapter).read()
    test_sentences = chapter2sentences(test_chapter)
    test_sents = [sentence_preprocess(s) for s in test_sentences]
    X_test = [sent2features(s) for s in test_sents]
    y_pred = crf.predict(X_test)
    dictNE = get_nes(y_pred, test_sents)
    print(dictNE('PERSON'))
    # listAllowedTypes = [ 'DATE', 'CARDINAL', 'ORDINAL', 'NORP' ]
    # listKeys = list( dictNE.keys() )
    # for strKey in listKeys :
    #     for nIndex in range(len(dictNE[strKey])) :
    #         dictNE[strKey][nIndex] = dictNE[strKey][nIndex].strip().lower()
    #     if not strKey in listAllowedTypes :
    #         del dictNE[strKey]

	# # write filtered NE dict
    # writeHandle = codecs.open( 'ne.json', 'w', 'utf-8', errors = 'replace' )
    # strJSON = json.dumps( dictNE, indent=2 )
    # writeHandle.write( strJSON + '\n' )
    # writeHandle.close()


x = exec_ner( file_chapter = 'comp3225_example_package\eval_chapter.txt', ontonotes_file = 'comp3225_example_package\ontonotes_parsed.json' )
