import re
import os
from pathlib import Path
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import gensim
from gensim import parsing
from gensim.models import CoherenceModel, TfidfModel
from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel
from gensim.models.hdpmodel import HdpModel
from gensim.test.utils import datapath
from preprocess_text import transformText

seed = 42
np.random.seed(seed)

df1 = pd.read_csv("../backend/data/book600k-700k.csv")
df2 = pd.read_csv("../backend/data/book700k-800k.csv")
df3 = pd.read_csv("../backend/data/book800k-900k.csv")
df3 = pd.read_csv("../backend/data/book900k-1000k.csv")
df4 = pd.read_csv("../backend/data/book1000k-1100k.csv")
df = pd.concat([df1, df2, df3, df4])
df = df[["Description", "Language", "Id"]]
df = df.dropna()
print(len(df))
text = list(df["Description"])
langs = list(df["Language"])
ids = list(df["Id"])

print(set(langs))

print("Transforming text")

text_dataset = list([transformText(t).strip().split() for t in list(text)])
bigram = gensim.models.Phrases(
    text_dataset, min_count=5, threshold=50
)  # higher threshold fewer phrases.
trigram = gensim.models.Phrases(bigram[text_dataset], threshold=50)
bigram_mod = gensim.models.phrases.Phraser(bigram)
trigram_mod = gensim.models.phrases.Phraser(trigram)


def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]


def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]


text_bigrams = make_bigrams(text_dataset)

text_dict = Dictionary(text_bigrams)
corpus = [text_dict.doc2bow(t) for t in text_bigrams]

print("Training Model")
num_topics = 100
lda = LdaModel(
    corpus=corpus,
    num_topics=num_topics,
    id2word=text_dict,
    alpha=0.1,
    eta=0.01,
    minimum_probability=0.0,
    random_state=seed,
)

temp_file = datapath(os.path.join(os.getcwd(), "model", "lda"))
lda.save(temp_file)

# temp_file = datapath(os.path.join(os.getcwd(), "model", f"lda"))
# lda = LdaModel.load(temp_file)

topics = lda.top_topics(corpus=corpus)
with open(f"topics.log", "w") as f:
    for idx, topic in enumerate(topics):
        f.write(f"Topic: {idx}, Score: {topic[1]}\n")
        for score, word in topic[0]:
            f.write(f"{word}, ")
        f.write("\n\n")

mat = np.zeros((len(corpus), num_topics))
for i, doc in enumerate(corpus):
    vec = lda.get_document_topics(doc, minimum_probability=0.0)
    mat[i] = np.array(vec)[:, 1]

import pickle

with open("lda_matrix.pkl", "wb") as f:
    pickle.dump(list(zip(ids, langs, mat)), f)
