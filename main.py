from Read_Docs import Read_data
from Word_net import unwanted_words, suicide_related_words
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from vectorizer import prepare_doc, create_freq_dict, computeTF, computeTFIDF, ComputeIDF
from n_grams import n_gram_vectorizer
from Word_net import word_net
from risk_moderate import check_nicotin_words, check_therapy_words
# from sentiment_analysis import analyse_sentiment_score
# from risk_moderate import compute_risk
stop_words = set(stopwords.words('english'))


def remove_unwanted_words(result_transcript):
    """
    this function clean the text based on a unrequired digit
    stop words etc
    :param result_transcript:
    :return:filtered text
    """
    cleaned_text = []
    final_text = []
    for sent in result_transcript:
        temp_words = []
        word_tokens = word_tokenize(sent)
        for word in word_tokens:
            if word not in stop_words:
                if word not in unwanted_words:
                    if not word.isdigit():
                        temp_words.append(word)
        cleaned_text.append(' '.join(word for word in temp_words))

    for text in cleaned_text:
        if text is not '':
            final_text.append(text)
    return final_text


def compute_report_score(scores):
    risk_level_score = 0
    for value in scores:
        for key, val in value.items():
            if val in suicide_related_words:
                risk_level_score += value['TFIDF_score']
    return risk_level_score


def analyse_text(filename, file_format):
    """
    read_Csv function takes filename as an argument and returns
    the filtered text by removing all the entities and unwanted tokens,values.
    n_gram_vectorizer will process all the text and divides the text
    into two pair of words  for deep analysis of the document.
    this function also compute the tf-idf scores for the text
    we will do the sentiment analysis of the document
    it will also check for the occurance of the high suicidal words
    :param filename:
    :return: the risk level for the patient
    """
    result_transcript = Read_data(filename, file_format, choose_index=1)
    # print("check this")
    # print(result_transcript)
    # exit()
    if result_transcript is None:
        return None
    final_text = remove_unwanted_words(result_transcript)
    # print(final_text)
    # print("final_text")
    ##comment this below
    # sentiment_score = analyse_sentiment_score(result_transcript)
    ##
    word_freq = word_net(final_text)
    # print(word_freq)
    doc_info = prepare_doc(final_text)
    # print(doc_info)
    ngram_features, bigram_features, trigram_features = n_gram_vectorizer(final_text)
    final_feature = [ngram_features, bigram_features, trigram_features]
    f = open("test.txt", "a")
    f.write(str(final_feature)+"\n")
    f.close()
    therapy_words = check_therapy_words(ngram_features, bigram_features, trigram_features)
    nicotin_words = check_nicotin_words(ngram_features, bigram_features, trigram_features)
    # print(ngram_features)
    # print("above this")
    ##comment
    # high_risk, suicide_related_words = check_high_suicidal_words(ngram_features)
    ##
    freqDict_list = create_freq_dict(final_text)
    # print(freqDict_list)
    TF_scores = computeTF(doc_info, freqDict_list)
    IDF_scores = ComputeIDF(doc_info, freqDict_list)
    scores = computeTFIDF(TF_scores, IDF_scores)
    # print(TF_scores, IDF_scores, scores)
    print(scores)
    ##comment below words
    # print(nicotin_words)
    if nicotin_words:
        nicotin_check = True
    else:
        nicotin_check = False
    if therapy_words:
        therapy_check = True
    else:
        therapy_check = False
    # risk_level_score = compute_report_score(scores)
    # risk_level_score += high_risk+ques_rel_risk
    ##
    # print('Risk level score {}% '.format(risk_level_score))
    # final_res = compute_risk(risk_level_score, sentiment_score, suicide_related_words, suicide_check)
    return nicotin_check, nicotin_words, therapy_check, therapy_words

#analyse_text(sys.argv[1])