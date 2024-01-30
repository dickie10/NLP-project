import pandas as pd 
import random
import os
import sys


from fever_doc_db import *

database = FeverDocDB()
# Replace 'your_file.jsonl' with the actual path to your JSONL file
jsonl_file = 'data/train.wiki7.jsonl'
count = 0
# Read the JSON Lines file into a pandas DataFrame
df = pd.read_json(jsonl_file, lines=True)

def get_whole_evidence(evidence_set):
    pos_sents = []
    for evidence in evidence_set:  
        page = evidence[2]
        doc_lines = database.get_doc_lines(page)
        doc_lines = get_valid_texts(doc_lines, page)
        for doc_line in doc_lines:
            if doc_line[2] == evidence[3]:
                pos_sents.append(doc_line[0])
    pos_sent = ' '.join(pos_sents)
    return pos_sent

def get_valid_texts(lines, page):
    if not lines:
        return []
    doc_lines = [doc_line.split("\t")[1] if len(doc_line.split("\t")[1]) > 1 else "" for doc_line in
                    lines.split("\n")]
    doc_lines = list(zip(doc_lines, [page] * len(doc_lines), range(len(doc_lines))))
    return doc_lines

def sampling(df, num_sample=1):

    

    X = []
    count = 0
    

    for index,line  in df.iterrows():
        count += 1 
        pos_pairs = []
        # count1 += 1
        if line['label'].upper() == "NOT ENOUGH INFO":
            continue
        neg_sents = []
        claim = line['claim'] 
        label = line['label']

        pos_set = set()
        for evidence_set in line['evidence']: 
            pos_sent = get_whole_evidence(evidence_set)
            if pos_sent in pos_set:
                continue
            pos_set.add(pos_sent)

        p_lines = []
        evidence_set = set(
            [(evidence[2], evidence[3]) for evidences in line['evidence'] for evidence in evidences])

        pages = [page for page in line['predicted_pages'] if page is not None]

        for page in pages:
            doc_lines = database.get_doc_lines(page)
            p_lines.extend(get_valid_texts(doc_lines, page))
        for doc_line in p_lines:
            if (doc_line[1], doc_line[2]) not in evidence_set:
                neg_sents.append(doc_line[0])

        num_sampling = num_sample
        if len(neg_sents) < num_sampling:
            num_sampling = len(neg_sents)
            # print(neg_sents)
        if num_sampling == 0:
            continue
        else:
            for pos_sent in pos_set:
                samples = random.sample(neg_sents, num_sampling)
                for sample in samples:
                    if not sample:
                        continue
                    X.append((claim, pos_sent, sample,label))
                    # if count % 1000 == 0:
                    #     print("claim:{} ,evidence :{} sample:{} label:{}".format(claim, pos_sent, sample,label))
    # Write data to TSV file
    with open("pos.tsv", 'w', encoding='utf-8') as f:
        f.write("index\tevidence\tclaim\tevidence_label\tlabel\n")
        for idx, (claim, pos_sent, _ ,label) in enumerate(X):
            f.write(f"{idx}\t[{pos_sent}]\t{claim}\tTrue\t{label}\n") 
    with open("neg.tsv", 'w', encoding='utf-8') as f:
        f.write("index\tevidence\tclaim\tevidence_label\tlabel\n")
        for idx, (claim,_,sample,_) in enumerate(X):
            f.write(f"{idx}\t[{sample}]\t{claim}\tFalse\tNOT ENOUGH INFO\n")
    return X  

X = sampling(df)


# def get_train_words(X):
#     claims = set()
#     sents = []
#     for claim, pos, neg in X:
#         claims.add(claim)
#         sents.append(pos)
#         sents.append(neg)

#     train_words = get_words(claims, sents)
#     print("training words processing done!")
#     return train_words


# def get_words(claims, sents):
#     h_max_length=20 
#     s_max_length=60
#     words = set()
#     for claim in claims:
#         for idx, word in enumerate(nltk_tokenizer(claim)):
#             if idx >= h_max_length:
#                 break
#             words.add(word.lower())
#     for sent in sents:
#         for idx, word in enumerate(nltk_tokenizer(sent)):
#             if idx >= s_max_length:
#                 break
#             words.add(word.lower())
#     return words 

# def nltk_tokenizer(sent):
#         # sent = sent_processing(sent)
#     return nltk.word_tokenize(sent)




# X = sampling(df) 
# print("chaljaa") 
# print(X[0]) 
# final_X = get_train_words(X[0]) 
# print("final X") 
# print(final_X) 


# def nltk_tokenizer(sent):
#     # sent = sent_processing(sent)
#     return nltk.word_tokenize(sent)


# def train_data_tokenizer(X_train): 

#     h_max_length=20 
#     s_max_length=60
#     claims = [claim for claim, _, _ in X_train]
#     pos_sents = [pos_sent for _, pos_sent, _ in X_train]
#     neg_sents = [neg_sent for _, _, neg_sent in X_train]

#     return claims, pos_sents,neg_sents

    # tokenized_claims, claims_lengths = proess_sents(claims,h_max_length)
    # tokenized_pos_sents, pos_sents_lengths = proess_sents(pos_sents, s_max_length)
    # tokenized_neg_sents, neg_sents_lengths = proess_sents(neg_sents, s_max_length)

    # new_claims = list(zip(tokenized_claims, claims_lengths))
    # new_pos_sents = list(zip(tokenized_pos_sents, pos_sents_lengths))
    # new_neg_sents = list(zip(tokenized_neg_sents, neg_sents_lengths))

#     return list(zip(new_claims, new_pos_sents, new_neg_sents)) 

# def proess_sents(sents,h_max_length):

#     tokenized_sents = []
#     sents_lengths = []
#     for sent in sents:
#         words = [word.lower() for word in nltk.word_tokenize(sent)]
#         if len(words) < h_max_length:
#             sents_lengths.append(len(words))
#             words.extend([""] * (h_max_length - len(words)))
#             tokenized_sents.append(words)
#         else:
#             sents_lengths.append(h_max_length)
#             words = words[:h_max_length]
#             tokenized_sents.append(words)
#     return tokenized_sents, sents_lengths 

#cliams, pos_sen, neg_sen = train_data_tokenizer(X) 
# print("data_file") 
# print(cliams)
# print("!!!!")
# print(pos_sen)
# print("!!!")
# print(neg_sen)
# print("Done!!!")