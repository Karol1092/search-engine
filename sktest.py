from sklearn.feature_extraction.text import TfidfVectorizer
import re
import numpy as np
from nltk.stem import PorterStemmer
from scipy.sparse import save_npz

stemmer = PorterStemmer()

def stem_analyzer(text):
    tokenized_text = re.findall(r"\w+", text.lower())
    stemmed_tokenized = [stemmer.stem(word) for word in tokenized_text]
    return " ".join(stemmed_tokenized)

corpus = [  
    'This is the first document.',
    'This document is the second document.',
    # 'And this is the third one.',
    'Is this the first document?',
]

stemmed = [stem_analyzer(text) for text in corpus]
print(stemmed)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(stemmed)
A = vectorizer.get_feature_names_out()
print(A)
print(X.toarray())

save_npz("matrix.npz", X)
