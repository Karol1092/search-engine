import joblib
import numpy as np
from nltk.stem import PorterStemmer
from scipy.sparse import load_npz
from make_matrix import stem
from sklearn.metrics.pairwise import cosine_similarity


class SearchEngine:
    def __init__(self, backends, k=10):
        self.backends = backends
        self.k = k
        
    def search(self, text, backend):
        backend = self.backends[backend]
        
        top, scores = backend.search(text, self.k)
        
        results = []
        for idx in top:
            results.append({
                "doc_id": int(idx + 1),
                "score": float(scores[idx])
            })
            
        return results
    
class TfidfBackend:
    def __init__(self, tfidf_path="tfidf.npz", vectorizer_path="tfidf-vectorizer.pkl"):
        self.tfidf = load_npz(tfidf_path)
        self.vectorizer = joblib.load(vectorizer_path)
        
    def search(self, text, k):
        processed_text = stem(text, PorterStemmer())
        q = self.vectorizer.transform([processed_text])
        
        scores = cosine_similarity(q, self.tfidf)[0]
        top = np.argsort(scores)[-k:][::-1]
        
        return top, scores
    
class LsaBackend:
    def __init__(self, lsa_path="lsa.npz", svd_path="svd_model.pkl", vectorizer_path="tfidf-vectorizer.pkl"):
        self.lsa = load_npz(lsa_path)
        self.svd = joblib.load(svd_path)
        self.vectorizer = joblib.load(vectorizer_path)
        
    def search(self, text, k):
        processed_text = stem(text, PorterStemmer())
        q = self.vectorizer.transform([processed_text])
        q_lsa = self.svd.transform(q)
        
        scores = cosine_similarity(q_lsa, self.lsa)[0]
        top = np.argsort(scores)[-k:][::-1]
        
        return top, scores
    