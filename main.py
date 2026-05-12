from scipy.sparse import load_npz

def main():
    tfidf = load_npz("tfidf.npz")
    
    print(tfidf)

    

if __name__ == "__main__":
    main()