from nltk.tokenize import word_tokenize

unwanted_words = [
    'need','talking','go','way','say','know','good','thats','think','group','order',
    'youve','youre','yeah','okay','saying','year','let','thank','oh','lot','going','theyre',
    'day','today','lets','dont','cant','put','whats','us','i','be','take','im','new','always',
    'made','one','take','got','um','every','see','also','people','right','it','is','like','get',
    'much','thinking','i','little','getting','maybe','default',
    'make','something','well','still','kind','bye','job','l','first','didnt','tell','want','would',
    'days','night','quarter','wont','three','fourth','great','seven','last','name','user','avatar',
    'hey','hi','theyll','there','yes','there','itll','id','youll','doesnt','next','sure','eight',
    'eighth','hadnt','four','fourth','five','fifth','six','sixth','seven','seventh','shes','havent','shall','hello','look','shall'
]

suicide_related_words = ['emotions', 'pain', 'depression', 'anxiety', 'sick', 'risk', 'humiliate', 'humiliation',
                          'darkness','threat', 'frustration', 'anger', 'frustrating', 'hurt',
                         'temptations', 'emotion', 'fear', 'anger', 'harm', 'shock']


def word_net(sentences):
    """
    thus function computes the repetition of a given word in a sentence
    :param sentences:
    :return: word_freq
    """
    word_freq = {}
    for sent in sentences:
        for word in word_tokenize(sent):
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1
    return word_freq