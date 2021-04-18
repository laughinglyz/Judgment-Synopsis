import csv
import json
import re

import nltk
import pandas as pd
from nltk.tokenize import sent_tokenize
from nltk.tokenize.punkt import PunktParameters
from tqdm import tqdm

# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('stopwords')

labels = ["CHARGE","TYPE_DRUGS","QUANTITY_DRUGS","QUANTITY_DRUGS_TOTAL",
"REFUGEE","REFUGEE_SENT","BAIL","BAIL_SENT","STREET","STREET_SENT","PERSISTENT","PERSISTENT_SENT","INTERNATIONAL","INTERNATIONAL_SENT","AGGREV_OTHER","AGGREV_OTHER_SENT",
"INDIVIDUAL_PENALTY","ALL_PENALTY","TRAINING_CENTER","DETENTION_CENTER","ADDICTION_TREATMENT_CENTER",
"PLEA_NOT_GUILTY","PLEA_GUILTY",
"REMORSE","REMORSE_SENT","SELF_CONSUME","SELF_CONSUME_SENT","CONTROLLED","CONTROLLED_SENT","TESTIMONY","TESTIMONY_SENT","GOOD_CHARACTER","GOOD_CHARACTER_SENT","MITIG_OTHER","MITIG_OTHER_SENT",
"YOUTH","PREVIOUS_CRIMINAL","CLEAR_RECORD","DRUG_ADDICT",
"STARTING_TARIFF","STARTING_TARIFF_COMBINED"]

label_rex = [re.compile('^OCC'),re.compile('^OT'),re.compile('^OQC'),re.compile('^OQT'),
re.compile('^ARC'),re.compile('^ARS'),re.compile('^ABC'),re.compile('^ABS'),re.compile('^ASC'),re.compile('^ASS'),re.compile('^APC'),re.compile('^APS'),re.compile('^AIC'),re.compile('^AIS'),re.compile('^AXC'),re.compile('^AXS'),
re.compile('^PI'),re.compile('^PA'),re.compile('^PT'),re.compile('^PD'),re.compile('^PM'),
re.compile('^PNC'),re.compile('^P[HD][0-5]'),
re.compile('^MRC'),re.compile('^MRS'),re.compile('^MSC'),re.compile('^MSS'),re.compile('^MCC'),re.compile('^MCS'),re.compile('^MYC'),re.compile('^MYS'),re.compile('^MGC'),re.compile('^MGS'),re.compile('^MXC'),re.compile('^MXS'),
re.compile('^BY'),re.compile('^BP'),re.compile('^BL'),re.compile('^BD'),
re.compile('^SPC'),re.compile('^SPD')
]

def match_label(label_doc):
    return [i for i,rex in enumerate(label_rex) if rex.search(label_doc)]

def check_overlap(i1,i2):
    return i1[0]<=i2[1] and i1[1]>=i2[0]

def extract_annotations(anno_dict):
    annotations,document_id = [],''
    for ant in anno_dict:
        if ant['label'][0] == "NC_NEUTRAL_CITATION":
            document_id = ant['points'][0]['text']
        else:
            for label in ant['label']:
                match_labels = match_label(label)
                if match_labels:
                    for p in ant['points']:
                        annotations.append((p['start'],p['end'],match_labels))
                    break
    return document_id,annotations

def classify(sentence,annotations):
    sent_class = [0]*len(labels)
    for start,end,match_labels in annotations:
        if check_overlap(sentence,(start,end)):
            for i in match_labels:
                sent_class[i] = 1
    return sent_class

def get_paragraphs(content):
    segmented_sign = re.compile('(\n[ ]*){2,}')
    all_sign = segmented_sign.finditer(content)
    paras,last_start = [],0
    for sign in all_sign:
        paras.append((last_start,sign.span()[0]-1))
        last_start = sign.span()[1]
    paras.append((last_start,len(content)-1))
    return paras

RAW_DATA_FILE = 'raw/drug_labeled_20200408.json'
OUTPUT_DATA_FILE = 'data/drug_features_classification.csv'
punkt_param = PunktParameters()
punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'miss', 'prof', 'inc','no','cap','nos','vol','para','exh'])
tokenizer = nltk.PunktSentenceTokenizer(punkt_param)

with open(RAW_DATA_FILE, 'r', encoding='UTF-8') as input_f:
    lines = input_f.readlines()
    with open(OUTPUT_DATA_FILE, 'w', encoding='UTF-8') as output_f:
        csv_writer = csv.writer(output_f)
        csv_writer.writerow(['neutral_citation','sentence_id','sentence']+labels)
        with tqdm(total=len(lines), unit_scale=True) as pbar:
            for document_count,line in enumerate(lines):
                data = json.loads(line)
                neutral_citation,annotations = extract_annotations(data["annotation"])
                if not neutral_citation: neutral_citation = document_count
                paras = get_paragraphs(data["content"])
                count = 0
                for para in paras:
                    content = data['content'][para[0]:para[1]+1]
                    for sent in tokenizer.span_tokenize(content):
                        sent_class = classify((sent[0]+para[0],sent[1]+para[0]),annotations)
                        csv_writer.writerow([neutral_citation,count,content[sent[0]:sent[1]+1]]+sent_class)
                        count+=1
                pbar.update()
    output_f.close()
input_f.close()