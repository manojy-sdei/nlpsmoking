import pandas as pd
from WordCloud import create_word_cloud
from collections import defaultdict
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import re
import webvtt
from risk_moderate import find_question_related_con
import sys

# initialisation
# #import pyttsx3
# engine = pyttsx3.init()

"""
read the csv file that contains the data 
for different conversation between patient and doctor
"""


def manage_multiple_session(data):
    patient_ids = []
    encounter_transcript = []
    temp = 0
    for patient_id, encounter_trans in zip(data['Encounter - Patient ID'], data['Encounter - Transcript']):
        ecounter = []
        ecounter.append(encounter_trans)
        if patient_id not in patient_ids:
            patient_ids.append(patient_id)
            encounter_transcript.append({'doc_id': temp, 'patient_id': patient_id, 'encounter_transcript': ecounter})
            temp += 1
        else:
            for records in encounter_transcript:
                if records['patient_id'] == patient_id:
                    records['encounter_transcript'].append(encounter_trans)
    return encounter_transcript


def remove_unwanted_items(text):
    filtered_text = re.sub('[^\w\s]', '', text)
    filtered_text = re.sub('_', '', filtered_text)
    filtered_text = re.sub('\s+', ' ', filtered_text)
    filtered_text = filtered_text.lower()
    filtered_text = filtered_text.strip()
    return filtered_text


def remove_unwanted_entities(text_sent):
    try:
        NER_Filtered = []
        for sent in text_sent:
            NER_check = False
            counts = defaultdict(int)
            sent_token = nltk.word_tokenize(sent)
            tagged = nltk.pos_tag(sent_token)
            entities = nltk.chunk.ne_chunk(tagged)
            if len(sent_token) <= 3:
                for token, tag in tagged:
                    counts[tag] += 0
                if '.' in counts:
                    counts.pop('.')
                if len(counts) is 1:
                    if 'NNP' or 'CD' or 'NN' in counts:
                        NER_check = True
                if len(counts) is 2:
                    if 'NNP' and 'NN' in counts:
                        NER_check = True
            if not NER_check:
                for tree in entities:
                    if hasattr(tree, 'label') and tree.label:
                        if tree.label() == 'PERSON':
                            for child in tree:
                                sent = sent.replace(child[0], '')
                    else:
                        if tree[1] == 'NNP':
                            sent = sent.replace(tree[0], '')
                if len(sent.strip()) is not 0:
                    NER_Filtered.append(sent)
        return NER_Filtered
    except Exception as e:
        print('error', e)


def identify_file_format_data(filename, file_format, choose_index):
    if file_format == 'text/csv':
        data = pd.read_csv(filename, encoding="ISO-8859-1")
        multiple_session_data = manage_multiple_session(data)
        if choose_index is not None:
            encounter_transcripts = [data['Encounter - Transcript'][choose_index]]
        else:
            encounter_transcripts = data['Encounter - Transcript']
        return encounter_transcripts, data
    if file_format == 'text/vtt':
        transcript = []
        data = None
        for caption in webvtt.read(filename):
            splited_text = caption.text.split(':')
            len_splited_text = len(splited_text)
            if len_splited_text > 2:
                transcript.append(caption.text)
            elif len_splited_text == 2:
                transcript.append(splited_text[1])
            else:
                transcript.append(splited_text[0])
        encounter_transcripts = [transcript]
        return encounter_transcripts, data


def Read_data(filename, file_format, choose_index=None):
    try:
        percent = 0
        result_transcript = None
        print('Processing Document.....')
        encounter_transcripts, data = identify_file_format_data(filename, file_format, choose_index)
        ques_rel_risk = find_question_related_con(encounter_transcripts)
        len_encounter_transcripts = len(encounter_transcripts)
        inrease_percent_by = 10 / (len_encounter_transcripts / 1000 * 100)
        for index, encounter_transcript in enumerate(encounter_transcripts):
            if len(encounter_transcript) > 1:
                if file_format == 'text/csv':
                    encounter_transcript = encounter_transcript.split('\r\n')
                filtered_transcript = remove_unwanted_entities(encounter_transcript)
                result_transcript = [remove_unwanted_items(transcript) for transcript in filtered_transcript]
                if data is not None:
                    patient_id = data['Encounter - Patient ID'][index]
                    # create_word_cloud(result_transcript, patient_id)
                    percent += inrease_percent_by
                    print('Record ID#:{} with Encounter - Patient ID:{} Processed Total: {}% Completed'
                          .format(data['Record ID#'][index], patient_id, percent))
                else:
                    print('Processed Total: {}% Completed'.format(inrease_percent_by))
        # for transcript in filtered_transcript:
        #     x = re.search("^([0-9][0-9])(:)([0-9][0-9])$", transcript)
        #     if x is None:
        #         print(transcript)
        #         engine.say(transcript)
        #         engine.runAndWait()
        return result_transcript, ques_rel_risk
    except Exception as e:
        print('Error', e)


    def get_building_id():
        try:
            print(system_ip)
            query = """select * from buildings where ai_server = '%s'""" %(system_ip)
            self.cur_COLOSQL.execute(query)
            rows = self.cur_COLOSQL.fetchall()
            for data in rows:
                building_id = data['building_id']
            return building_id
        except:
            self.db_conn_COLOSQL.rollback()
            logging.debug("error in selecting building_id" + str(traceback.format_exc()))

