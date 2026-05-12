import joblib
import sqlite3
import numpy as np
from nltk.stem import PorterStemmer
from scipy.sparse import load_npz
from make_matrix import stem
from sklearn.metrics.pairwise import cosine_similarity

K = 10

def main():
    tfidf = load_npz("tfidf.npz")
    vectorizer = joblib.load("tfidf-vectorizer.pkl")

    stemmer = PorterStemmer()
    
    while True:
        text = input("Search: ")
        processed_text = stem(text, stemmer)
        
        q = vectorizer.transform([processed_text])
        
        scores = cosine_similarity(q, tfidf)[0]
        
        top_indeces = np.argsort(scores)[-K:][::-1]
        
        print("\n")
        
        for idx in top_indeces:
            doc_title, doc_url = get_doc_title_url(str(idx + 1))
            print(doc_title.replace("_", " "))
            print(doc_url)
            print(f"{(scores[idx] * 100):.1f}%", "\n")
            
        print("\n")
    
    
def get_doc_title_url(doc_id):
    conn = sqlite3.connect("articles.db")
    cur = conn.cursor()
    
    cur.execute("SELECT title, url FROM articles WHERE id = ?", (doc_id,))
    row = cur.fetchone()
    
    conn.close()
    
    return row[0], row[1]

if __name__ == "__main__":
    main()