import csv
import json
import re

import nltk
import pandas as pd
from nltk.tokenize import sent_tokenize
from nltk.tokenize.punkt import PunktParameters

# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('stopwords')


def extract_annotations(anno_dict):
    annotations,document_id = [],''
    for ant in anno_dict:
        if ant['label'][0] == "NC_NEUTRAL_CITATION":
            document_id = ant['points'][0]['text']
            print(document_id)
        else:
            for p in ant['points']:
                annotations.append((p['start'],p['end']))
    annotations.sort()
    arr,last = [],-1
    for start,end in annotations:
        if start>last:
            arr.append([start,end])
        else:
            arr[-1][-1] = last = max(end,last)
    return document_id,arr

def classify(sentence,annotations,i):
    while i<len(annotations) and sentence[0]>annotations[i][1]:
        i+=1
    if i == len(annotations): return False,i
    if sentence[1] >= annotations[i][0]: return True,i
    return False,i

def get_paras(content):
    segmented_sign = re.compile('(\n[ ]*){2,}')
    all_sign = segmented_sign.finditer(content)
    paras,last_start = [],0
    for sign in all_sign:
        paras.append((last_start,sign.span()[0]-1))
        last_start = sign.span()[1]
    paras.append((last_start,len(content)-1))
    return paras

RAW_DATA_FILE = 'raw/drug_labeled_20200408.json'
OUTPUT_DATA_FILE = 'data/drug_sentence_classification.csv'
punkt_param = PunktParameters()
punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'miss', 'prof', 'inc','no','cap','nos','vol','para','exh'])
tokenizer = nltk.PunktSentenceTokenizer(punkt_param)

with open(RAW_DATA_FILE, 'r', encoding='UTF-8') as input_f:
    lines = input_f.readlines()
    with open(OUTPUT_DATA_FILE, 'w', encoding='UTF-8') as output_f:
        csv_writer = csv.writer(output_f)
        csv_writer.writerow(['neutral_citation','sentence_id','important','sentence'])
        for document_count,line in enumerate(lines):
            data = json.loads(line)
            neutral_citation,annotations = extract_annotations(data["annotation"])
            if not neutral_citation: neutral_citation = document_count
            paras = get_paras(data["content"])
            i,count = 0,0
            for para in paras:
                content = data['content'][para[0]:para[1]+1]
                for sent in tokenizer.span_tokenize(content):
                    sent_type,i = classify((sent[0]+para[0],sent[1]+para[0]),annotations,i)
                    csv_writer.writerow([neutral_citation,count,sent_type,content[sent[0]:sent[1]+1]])
                    count+=1