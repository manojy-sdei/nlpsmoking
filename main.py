from Read_Docs import Read_data
from Word_net import unwanted_words, suicide_related_words
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from vectorizer import prepare_doc, create_freq_dict, computeTF, computeTFIDF, ComputeIDF
from n_grams import n_gram_vectorizer
from Word_net import word_net
from risk_moderate import check_nicotin_words, check_therapy_words, check_high_suicidal_words, check_sucide_monitering
from sentiment_analysis import analyse_sentiment_score
from risk_moderate import compute_risk
from risk_moderate import find_question_related_con_change
import ast

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
    result_transcript, ques_rel_risk = Read_data(filename, file_format, choose_index=1)
    # print("check this")
    # print(result_transcript)
    # exit()
    #print(result_transcript)
    if result_transcript is None:
        return None
    final_text = remove_unwanted_words(result_transcript)
    sentiment_score, pos, neg = analyse_sentiment_score(result_transcript)
    word_freq = word_net(final_text)
    doc_info = prepare_doc(final_text)
    ngram_features, bigram_features, trigram_features = n_gram_vectorizer(final_text)
    high_risk, suicide_related_words = check_high_suicidal_words(bigram_features)
    # f = open("test.txt", "a")
    # f.write(str(final_feature)+"\n")
    # f.close()
    therapy_words = check_therapy_words(ngram_features, bigram_features, trigram_features)
    nicotin_words = check_nicotin_words(ngram_features, bigram_features, trigram_features)
    freqDict_list = create_freq_dict(final_text)
    TF_scores = computeTF(doc_info, freqDict_list)
    IDF_scores = ComputeIDF(doc_info, freqDict_list)
    scores = computeTFIDF(TF_scores, IDF_scores)
    if nicotin_words:
        nicotin_check = True
    else:
        nicotin_check = False
    if therapy_words:
        therapy_check = True
    else:
        therapy_check = False
    suicide_check = check_sucide_monitering(scores, ngram_features)
    risk_level_score = compute_report_score(scores)
    risk_level_score += high_risk + ques_rel_risk
    print('Risk level score {}% '.format(risk_level_score))
    final_res = compute_risk(risk_level_score, sentiment_score, suicide_related_words, suicide_check)
    return nicotin_check, nicotin_words, therapy_check, therapy_words, final_res


def analyse_text_data(filename, file_format):
    result_transcript, ques_rel_risk = Read_data(filename, file_format, choose_index=1)
    # print("check this")
    #print(result_transcript)
    # exit()
    # print("vtt_data:-" + vtt_data)
    # result_transcript = ast.literal_eval(vtt_data)
    # ques_rel_risk = find_question_related_con_change(list(result_transcript))
    # print("result_transcripts:-" + str(result_transcript))
    # print(result_transcript)
    if result_transcript is None:
        return None
    final_text = remove_unwanted_words(result_transcript)
    sentiment_score, pos, neg = analyse_sentiment_score(result_transcript)
    word_freq = word_net(final_text)
    doc_info = prepare_doc(final_text)
    ngram_features, bigram_features, trigram_features = n_gram_vectorizer(final_text)
    high_risk, suicide_related_words = check_high_suicidal_words(ngram_features)
    # f = open("test.txt", "a")
    # f.write(str(final_feature)+"\n")
    # f.close()
    therapy_words = check_therapy_words(ngram_features, bigram_features, trigram_features)
    nicotin_words = check_nicotin_words(ngram_features, bigram_features, trigram_features)
    freqDict_list = create_freq_dict(final_text)
    TF_scores = computeTF(doc_info, freqDict_list)
    IDF_scores = ComputeIDF(doc_info, freqDict_list)
    scores = computeTFIDF(TF_scores, IDF_scores)
    if nicotin_words:
        nicotin_check = True
    else:
        nicotin_check = False
    if therapy_words:
        therapy_check = True
    else:
        therapy_check = False
    suicide_check = check_sucide_monitering(scores, ngram_features)
    risk_level_score = compute_report_score(scores)
    risk_level_score += high_risk + ques_rel_risk
    print('Risk level score {}% '.format(risk_level_score))
    suicide_monitering_check, risk, sentiment_score, suicide_related_words = compute_risk(risk_level_score, sentiment_score, suicide_related_words, suicide_check)
    return nicotin_check, nicotin_words, therapy_check, therapy_words, suicide_monitering_check, risk, pos, neg, suicide_related_words
# analyse_text(sys.argv[1])
