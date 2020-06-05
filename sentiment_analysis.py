from textblob import TextBlob
import nltk
#from safet.stem_lemma import apply_stemmer


def prepare_formulae(pos, neg):
    total = pos+neg
    pos = pos/total*100
    neg = neg/total*100
    return pos, neg


def analyse_sentiment_score(sentences):
    """

    :param sentences:
    :return:
    """
    sentiment_score = {}
    pos = 0
    neg = 0
    #filtered_sentences = apply_stemmer(sentences)
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        if len(words)>2:
            output = TextBlob(sentence).sentiment

            if output[0] >= 0:
                pos += 1
            else:
                neg += 1
    pos, neg = prepare_formulae(pos, neg)
    sentiment_score['pos_analysis'] = pos
    sentiment_score['neg_analysis'] = neg
    return sentiment_score