import joblib
import numpy as np
from nltk.stem import PorterStemmer
from scipy.sparse import load_npz
from make_matrix import stem
from sklearn.metrics.pairwise import cosine_similarity

class SearchEngine:
    def __init__(self, tfidf_path, vectorizer_path, k=10):
        self.tfidf = load_npz(tfidf_path)
        self.vectorizer = joblib.load(vectorizer_path)
        self.stemmer = PorterStemmer()
        self.k = k

    def search(self, text):
        processed_text = stem(text, self.stemmer)
        q = self.vectorizer.transform([processed_text])
        
        scores = cosine_similarity(q, self.tfidf)[0]
        top_indices = np.argsort(scores)[-self.k:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                "doc_id": int(idx + 1),
                "score": float(scores[idx])
            })
            
        return results

