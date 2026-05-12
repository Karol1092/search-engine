import json
import sqlite3
import re
import numpy as np
from nltk.stem import PorterStemmer
from scipy.sparse import load_npz
from make_matrix import stem
from sklearn.feature_extraction.text import TfidfVectorizer

def main():
    tfidf = load_npz("tfidf.npz")

    stemmer = PorterStemmer()

    text = input()
    
    processed_text = [stem(text, stemmer)]
    
    with open("vocab.json", "r", encoding="utf-8") as f:
        vocab = json.load(f)
        
    print(type(vocab))
    
    vectorizer = TfidfVectorizer(
        min_df=5,
        stop_words="english",
        dtype=np.float32,
    )
    
    

    

if __name__ == "__main__":
    main()