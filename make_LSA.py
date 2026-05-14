import joblib
from sklearn.decomposition import TruncatedSVD
from scipy.sparse import load_npz, save_npz, csr_matrix


def main():
    tfidf = load_npz("tfidf.npz")

    svd = TruncatedSVD(n_components=400)
    
    lsa = svd.fit_transform(tfidf)
    
    save_npz("lsa.npz", csr_matrix(lsa))
    joblib.dump(svd, "svd_model.pkl")
     
    
if __name__ == "__main__":
    main()