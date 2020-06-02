from nltk.tokenize import word_tokenize
import math


def count_words(sent):
    count = 0
    words = word_tokenize(sent)
    for word in words:
        count += 1
    return count


def prepare_doc(text_sent):
    doc_info = []
    i = 0
    for sent in text_sent:
        i += 1
        count = count_words(sent)
        temp = {'doc_id': i, 'doc_length': count}
        doc_info.append(temp)
    return doc_info


def create_freq_dict(sents):
    i = 0
    freqDict_list = []
    for sent in sents:
        i += 1
        freq_dict = {}
        words = word_tokenize(sent)
        for word in words:
            word = word.lower()
            if word in freq_dict:
                freq_dict[word] += 1
            else:
                freq_dict[word] = 1
            temp = {'doc_id': i, 'freq_dict': freq_dict}
        freqDict_list.append(temp)
    return freqDict_list


def computeTF(doc_info, freqDict_list):
    TF_scores = []
    for temp_dict in freqDict_list:
        id = temp_dict['doc_id']
        for k in temp_dict['freq_dict']:
            temp = {'doc_id': id,
                    'TF_score': temp_dict['freq_dict'][k]/doc_info[id-1]['doc_length'],
                    'key': k
                  }
            TF_scores.append(temp)
    return TF_scores


def ComputeIDF(doc_info,freqDict_list):
    IDF_scores = []
    counter = 0
    for dictn in freqDict_list:
        counter += 1
        for k in dictn['freq_dict'].keys():
            count = sum([k in tempDict['freq_dict'] for tempDict in freqDict_list])
            temp = {'doc_id': counter, 'IDF_score': math.log(len(doc_info)/count), 'key': k}
            IDF_scores.append(temp)
    return IDF_scores


def computeTFIDF(TF_scores, IDF_scores):
    TFIDF_scores = []
    for i in IDF_scores:
        for j in TF_scores:
            if i['key'] == j['key'] and i['doc_id'] == j['doc_id']:
                temp = {'doc_id': i['doc_id'],
                        'TFIDF_score': i['IDF_score']*j['TF_score'],
                        'key': j['key']}
        TFIDF_scores.append(temp)
    return TFIDF_scores