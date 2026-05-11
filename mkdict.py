import numpy as np
import sqlite3
import re
import nltk
import json
from nltk.corpus import names, stopwords, words
from nltk.stem.porter import PorterStemmer
from collections import defaultdict

nltk.data.path.append(".nltk_data")

def main():
    conn = sqlite3.connect("articles.db")
    cur = conn.cursor()
    
    cur.execute("SELECT text FROM articles")

    df = defaultdict(int)
    
    for i, row in enumerate(cur): 
        if i % 10000 == 0:
            print(f"step {i}")
        
        text = row[0]
        processed_text = process_text(text)
        unique_tokens = set(processed_text)
        
        for t in unique_tokens:
            df[t] += 1
        
    
    values = np.array(list(df.values()))
    print(f"Number of all words: {len(values)}")

    filtered = {w: c for w, c in df.items() if 3 < c}
    print(f"Number of filtered words: {len(filtered)}")
    
    vocab = {w: idx for idx, (w, _) in enumerate(filtered.items())}
    
    with open("vocab.json", "w") as f:
        json.dump(vocab, f)
    
    with open("df.json", "w") as f:
        json.dump(filtered, f)
    
    
    
    
    
def process_text(text):
    tokenized_text = re.findall(r"\w+", text.lower())
    filtered_text = remove_stopwords(tokenized_text)
    stemmed_text = stem(filtered_text)
    return stemmed_text
    
    
def remove_stopwords(tokenized_text):
    stops = set(stopwords.words("english"))
    filtered = [t for t in tokenized_text if t not in stops]
    return filtered
    
def stem(tokenized_text):
    stemmer = PorterStemmer()
    singles = [stemmer.stem(t) for t in tokenized_text]
    return singles

if __name__ == "__main__":
    main()