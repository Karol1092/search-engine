import joblib
import sqlite3
import re
import numpy as np
from nltk.stem import PorterStemmer
from scipy.sparse import save_npz
from sklearn.feature_extraction.text import TfidfVectorizer


def main():
    vectorizer = TfidfVectorizer(
        min_df=5,
        stop_words="english",
        dtype=np.float32
    )
    
    tfidf = vectorizer.fit_transform(doc_generator("articles.db"))
    A = vectorizer.vocabulary_
    print(f"Vocabulary size: {len(A)}")
    
    save_npz("tfidf.npz", tfidf)
    joblib.dump(vectorizer, "tfidf-vectorizer.pkl")


def doc_generator(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT text FROM articles ORDER BY id")
    
    stemmer = PorterStemmer()
    
    for i, (text, ) in enumerate(cursor):
        if i % 10000 == 0:
            print(f"step {i}")
        
        processed_text = stem(text, stemmer)
        yield processed_text
        
    conn.close()
    
def stem(text, stemmer):
    tokenized_text = re.findall(r"\w+", text.lower())
    stemmed = [stemmer.stem(word) for word in tokenized_text]
    return " ".join(stemmed)

if __name__ == "__main__":
    main()