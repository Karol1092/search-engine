import joblib
import sqlite3
import re
import numpy as np
from nltk.stem import PorterStemmer
from scipy.sparse import load_npz
from make_matrix import stem
from sklearn.feature_extraction.text import TfidfVectorizer

def main():
    tfidf = load_npz("tfidf.npz")
    vectorizer = joblib.load("tfidf-vectorizer.pkl")

    stemmer = PorterStemmer()
    text = input()
    processed_text = stem(text, stemmer)
    
    print(processed_text)
    
    
    q = vectorizer.transform([processed_text])
    
    print(q)
    

if __name__ == "__main__":
    main()