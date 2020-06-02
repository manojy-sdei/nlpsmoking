from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from datetime import datetime
stopwords = set(STOPWORDS)


def show_wordcloud(data, title=None):
    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        max_words=200,
        max_font_size=40,
        scale=3,
        random_state=1  # chosen at random by flipping a coin; it was heads
    ).generate(str(data))

    # fig = plt.figure(1, figsize=(12, 12))
    # plt.axis('off')
    # if title:
    #     fig.suptitle(title, fontsize=20)
    #     fig.subplots_adjust(top=2.3)
    #
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.show()
    return wordcloud


def create_word_cloud(cleaned_data, patient_id):
    cloud_data = ' '.join(sentence for sentence in cleaned_data)
    word_cloud = show_wordcloud(cloud_data)
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%H%M%S")
    word_cloud.to_file("E:\SAFE-T\images\{}.png".format('Patient_ID_' + timestampStr+'_'+str(patient_id)))
