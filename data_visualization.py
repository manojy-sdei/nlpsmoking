from risk_moderate import suicide_monitering_check,high_risk_words
import pandas as pd
import matplotlib.pyplot as plt


def risk_analysis_visualization(word_freq, bigram_features):
    final_visual_risk = []
    for word in suicide_monitering_check['RISK_FACTORS']:
        if word in word_freq:
            final_visual_risk.append([word, word_freq[word]])
        elif word in bigram_features:
            if word in final_visual_risk:
                final_visual_risk[word] += 1
            else:
                final_visual_risk.append([word, 1])
        elif word in high_risk_words:
            if word in final_visual_risk:
                final_visual_risk[word] += 1
            else:
                final_visual_risk.append([word, 1])
        else:
            final_visual_risk.append([word, 0])

        words_df_risk = pd.DataFrame(final_visual_risk, columns=['RISK_FACTORS', 'FREQ'])
        words_df_risk.plot(x="RISK_FACTORS", y='FREQ', kind="bar")
        plt.savefig('risk1.png')
        words_df_risk.plot(figsize=(10, 5))
        plt.savefig('risk2.png')


def protective_visualization(word_freq,bigram_features):
    final_visual_protective = []
    for word in suicide_monitering_check['PROTECTIVE_FACTORS']:
        if word in word_freq:
            final_visual_protective.append([word, word_freq[word]])
        elif word in bigram_features:
            if word in final_visual_protective:
                final_visual_protective[word] += 1
            else:
                final_visual_protective.append([word, 1])
        else:
            final_visual_protective.append([word, 0])
    words_df_risk = pd.DataFrame(final_visual_protective, columns=['PROTECTIVE_FACTORS', 'FREQ'])
    words_df_risk.plot(x="RISK_FACTORS", y='FREQ', kind="bar")
    plt.savefig('protective1.png')
    words_df_risk.plot(figsize=(10, 5))
    plt.savefig('protective2.png')


def suicide_visualization(word_freq, bigram_features):
    final_visual_enquiry = []
    for word in suicide_monitering_check['SUICIDE_INQUIRY']:
        if word in word_freq:
            final_visual_enquiry.append([word, word_freq[word]])
        elif word in bigram_features:
            if word in final_visual_enquiry:
                final_visual_enquiry[word] += 1
            final_visual_enquiry.append([word, 1])
        else:
            final_visual_enquiry.append([word, 0])

    words_df_risk = pd.DataFrame(final_visual_enquiry, columns=['SUICIDE_INQUIRY', 'FREQ'])
    words_df_risk.plot(x="RISK_FACTORS", y='FREQ', kind="bar")
    plt.savefig('enquiry1.png')
    words_df_risk.plot(figsize=(10, 5))
    plt.savefig('enquiry2.png')


def visualize_data(word_freq, bigram_features):
    risk_analysis_visualization(word_freq, bigram_features)
    protective_visualization(word_freq, bigram_features)
    suicide_visualization(word_freq, bigram_features)