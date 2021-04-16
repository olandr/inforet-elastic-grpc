import re
import os
from pathlib import Path
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import nltk
from nltk.corpus import stopwords
import gensim
from gensim import parsing
from gensim.models import CoherenceModel
from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel
from gensim.models.hdpmodel import HdpModel
from gensim.test.utils import datapath

new_stop_words = [
"get",
"way",
"because",
"page",
"people",
"people's",
"easy",
"easier",
"need",
"make",
"use",
"using",
"useful",
"like",
"i'm",
"became",
"could",
"wish"
]

def transformText(text):
    stops = set(stopwords.words("english"))
    stops.update(new_stop_words)
    # Convert text to lower
    text = text.lower()
    # Removing non ASCII chars
    text = re.sub(r'[^\x00-\x7f]',r' ',text)
    # Remove the punctuation
    text = gensim.parsing.preprocessing.strip_punctuation2(text)
    # Strip all the numerics
    text = gensim.parsing.preprocessing.strip_numeric(text)
    # Strip multiple whitespaces
    text = gensim.corpora.textcorpus.strip_multiple_whitespaces(text)
    #for rem in rem_list:
    #    text = text.replace(rem.lower(), '')
    text = gensim.corpora.textcorpus.strip_multiple_whitespaces(text)
    text = text.replace(" ui ", " user interface ")
    text = text.replace(" ux ", " user experience ")
    # Removing all the stopwords
    filtered_words = [word for word in text.split() if word not in stops]
    # Removing all the tokens with lesser than 3 characters
    filtered_words = gensim.corpora.textcorpus.remove_short(filtered_words, minsize=3)
    # Preprocessed text after stop words removal
    text = " ".join(filtered_words)
    # Strip multiple whitespaces
    text = gensim.corpora.textcorpus.strip_multiple_whitespaces(text)
    # Stemming
    return gensim.parsing.preprocessing.stem_text(text)