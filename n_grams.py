from sklearn.feature_extraction.text import CountVectorizer


def n_gram_vectorizer(sentences, n_gram_value=(1, 1)):
    """
    this function compute the bigram,trigram,n-gram, unigram
    vectorizer values from the given text
    :param sentences:
    :param n_gram_value:
    :return: n-gram sentences
    """
    val1 = n_gram_value[0]
    val2 = n_gram_value[1]
    vectorizer = CountVectorizer(ngram_range=(val1, val2))
    # print(vectorizer)
    X1 = vectorizer.fit_transform(sentences)
    monogram_features = (vectorizer.get_feature_names())
    vectorizer_2 = CountVectorizer(ngram_range=(2, 2))
    X2 = vectorizer_2.fit_transform(sentences)
    bigram_features = (vectorizer_2.get_feature_names())
    vectorizer_3 = CountVectorizer(ngram_range=(3, 3))
    X3 = vectorizer_3.fit_transform(sentences)
    trigram_features = (vectorizer_3.get_feature_names())
    return monogram_features, bigram_features, trigram_features

