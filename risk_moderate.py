from nltk.tokenize import word_tokenize

high_risk_words = ['panic attack', 'freaking out', 'high risk', 'self harm', 'self awareness', 'self reflection','hurting yourself',
                   'anxiety attacks', 'hot flashes', 'suicide', 'kill myself', 'die','died', 'want to die', 'commit suicide', 'suicide attempts', 'hurt myself', 'suicide attempts', 'suicide attempt', 'abuse myself']

suicide_monitering_check = {
    'RISK_FACTORS': ['self harm', 'self injuries', 'injuries', 'suicide attempts', 'aborted', 'prior', 'alcohol',
                     'adhd', 'tbi', 'ptsd', 'antisocial behaviours', 'aggression', 'impulsivity', 'anhedonia',
                     'hopelessness', 'anxiety', 'panic', 'insomnia', 'hallucinations', 'humiliation', 'shame',
                     'despair', 'humiliate', 'anger', 'fear', 'pain', 'intoxication', 'turmoil', 'chaos', 'hurt',
                     'physical abuse', 'sexual abuse', 'abuse', 'social isolation', 'isolation', 'depression',
                     'frustration', 'frustrating''unwise', 'temptations', 'harm', 'darkness', 'shock', 'sick',
                     'provider', 'treatment change', 'co morbidity', 'morbidity', 'lawlessness', 'riot'],
    'PROTECTIVE_FACTORS': ['cope', 'stress', 'religious beliefs', 'beliefs', 'believe', 'tolerance',
                           'frustration tolerance', 'social supports'],
    'SUICIDE_INQUIRY': ['thoughts', 'frequency', 'intensity', 'plans', 'behaviour', 'intent', 'ideas'
                                                                                              'attempts',
                        'past attempts', 'aborted attempts', 'rehearsals']
}

nicotin_words = ['nicotine', 'cigarettes', 'chew', 'vape', 'vape pen', 'juul', 'tobacco', 'smoking', 'smoke', 'dipping',
                 ' e-cigarette', 'chewing', 'chewed', 'cigarette']

therapy_words = ['cessation', 'stopping', 'quitting', 'benefits of quitting', 'benefits of smoking cessation',
                 'challenges of quitting', 'barriers of quitting', 'challenges with stopping', 'barriers to stopping',
                 'risks of smoking', 'risks of vaping', 'risks of nicotine', 'Bupropion', 'sustained release',
                 'Varenicline', 'Nicotine gum', 'Nicotine inhaler', 'Nicotine lozenge', 'Nicotine patch', 'Nicotrol',
                 'Nasal spray', 'lozenge', 'gum', 'Chantix', 'Wellbutrin', 'Zyban', 'nicotine placebo', 'marijuana card']

# therapy_intervention = {
#     "Ask": "['', '', '']",
#     "Advice": "['', '', '']",
#     "Assess": "['']",
#     "Assist": "['']",
#     "Arrange": "['']",
# }


def check_nicotin_words(n_gram_vectorizer, bigram_vectorizer, trigram_vectorizer):
    # high_risk = 0
    nicotin_related_word = []
    #print(n_gram_vectorizer)
    #print(bigram_vectorizer)
    #print(trigram_vectorizer)
    for paired_words in n_gram_vectorizer:
        if paired_words in nicotin_words:
            nicotin_related_word.append(paired_words)
    for words in bigram_vectorizer:
        if words in nicotin_words:
            nicotin_related_word.append(words)
    for words in trigram_vectorizer:
        if words in nicotin_words:
            nicotin_related_word.append(words)
    #print("this is the nicotin_words" + str(nicotin_related_word))
    return nicotin_related_word


def check_therapy_words(n_gram_vectorizer, bigram_vectorizer, trigram_vectorizer):
    # high_risk = 0
    thrapy_related_word = []
    for paired_words in n_gram_vectorizer:
        if paired_words in therapy_words:
            thrapy_related_word.append(paired_words)
    for words in bigram_vectorizer:
        if words in therapy_words:
            thrapy_related_word.append(words)
    for words in trigram_vectorizer:
        if words in therapy_words:
            thrapy_related_word.append(words)
    return thrapy_related_word


def check_sucide_monitering(scores, ngram_features):
    risk_score = 0
    protective_score = 0
    suicide_score = 0
    for score in scores:
        if score['key'] in suicide_monitering_check['RISK_FACTORS']:
            risk_score += 1
        if score['key'] in suicide_monitering_check['PROTECTIVE_FACTORS']:
            protective_score += 1
        if score['key'] in suicide_monitering_check['SUICIDE_INQUIRY']:
            suicide_score += 1
    for feature in ngram_features:
        if feature in suicide_monitering_check['RISK_FACTORS']:
            risk_score += 1
        if feature in suicide_monitering_check['PROTECTIVE_FACTORS']:
            protective_score += 1
        if feature in suicide_monitering_check['SUICIDE_INQUIRY']:
            suicide_score += 1
    risk_percent = risk_score / len(suicide_monitering_check['RISK_FACTORS']) * 100
    protective_percent = protective_score / len(suicide_monitering_check['PROTECTIVE_FACTORS']) * 100
    suicide_percent = suicide_score / len(suicide_monitering_check['SUICIDE_INQUIRY']) * 100
    if risk_percent >= 50.0 and protective_percent >= 50.0 and suicide_percent >= 50.0:
        suicide_monitering_check_result = True
    else:
        suicide_monitering_check_result = False
    return suicide_monitering_check_result


def risk_level(risk_score):
    """
    this function set the global values to determine
    the risk at high ,low,moderate level.
    :param risk_score:
    :return:
    """
    if risk_score < 35.0:
        risk = 'LOW'
    elif risk_score < 65.0:
        risk = 'MODERATE'
    else:
        risk = 'HIGH'
    return risk


def compute_risk(risk_val, sentiment_score, suicide_related_words, suicide_monitering_check):
    """
    this function prepare the final data or the api
    :param risk_val:
    :param sentiment_score:
    :return: risk data
    """
    # risk_data = []
    risk = risk_level(risk_val)
    # risk_data.append({
    #     '77': suicide_monitering_check, #suicide_monitering_check
    #     '78': risk, #risk_level
    #     '93': sentiment_score, #sentiment_score
    #     '94': suicide_related_words #suicide_related_words
    # })
    return suicide_monitering_check, risk, sentiment_score, suicide_related_words


def check_high_suicidal_words(n_gram_vectorizer, bi_gram_vectorizer, tri_gram_vectorizer):
    """
    this function identified the high suicidal risk words in the sentences
    as we have some of the predefined words through which we can compute the
    we also sae those words which will found in the sentences
    :param n_gram_vectorizer:
    :return:
    """
    high_risk = 0
    suicide_related_word = []
    for paired_words in n_gram_vectorizer:
        if paired_words in high_risk_words:
            high_risk += 10
            suicide_related_word.append(paired_words)
    for paired_words in bi_gram_vectorizer:
        if paired_words in high_risk_words:
            high_risk += 10
            suicide_related_word.append(paired_words)
    for paired_words in tri_gram_vectorizer:
        if paired_words in high_risk_words:
            high_risk += 10
            suicide_related_word.append(paired_words)
    return high_risk, suicide_related_word


def compute_question_based_risk(check_tokens):
    risk = 0
    for word in word_tokenize(check_tokens.lower()):
        if word in ['yeah', 'yes']:
            risk += 20
    return risk


def find_question_related_con(transcript):
    total_risk = 0
    for index, sent in enumerate(transcript[0]):
        word_tokens = word_tokenize(sent)
        if 'suicide' in word_tokens:
            risk = compute_question_based_risk(transcript[0][index + 1])
            total_risk += risk
        if 'self' in word_tokens:
            if 'harm' in word_tokens:
                risk = compute_question_based_risk(transcript[0][index + 1])
                total_risk += risk
            if 'hurt' in word_tokens:
                risk = compute_question_based_risk(transcript[0][index + 1])
                total_risk += risk
    return total_risk


def find_question_related_con_change(transcript):
    total_risk = 0
    for index, sent in enumerate(transcript[0]):
        word_tokens = word_tokenize(sent)
        if 'suicide' in word_tokens:
            risk = compute_question_based_risk(transcript[0][index + 1])
            total_risk += risk
        if 'self' in word_tokens:
            if 'harm' in word_tokens:
                risk = compute_question_based_risk(transcript[0][index + 1])
                total_risk += risk
            if 'hurt' in word_tokens:
                risk = compute_question_based_risk(transcript[0][index + 1])
                total_risk += risk
    return total_risk
