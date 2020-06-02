from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
porter = PorterStemmer()


def apply_stemmer(sentences):
    """
    this function perform the text filtering for finding
    the stem and lemmatization of a words in different sentences
    to make the sentence analyse more accurately
    by the sentiment model
    stem is to reduce the sentence to to (pseudo)stems
    lemmatization reduces the word-forms to linguistically valid lemmas
    :param sentences:
    :return:stem_lema sent
    """
    stem_lemma_sentence = []
    for sentence in sentences:
        token_words = word_tokenize(sentence)
        temp_sentence = []
        for word in token_words:
            word = porter.stem(word)
            temp_sentence.append(porter.stem(word))
            temp_sentence.append(" ")
        stem_lemma_sentence.append("".join(temp_sentence))
    return stem_lemma_sentence
