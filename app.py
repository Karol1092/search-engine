from fastapi import FastAPI
from search_engine import SearchEngine
from db import get_docs_by_id

app = FastAPI()

search_engine = SearchEngine(
    "tfidf.npz", 
    "tfidf-vectorizer.pkl", 
    k=10
)

final_results = []

@app.post("/search")
async def search(q: str):
    results = search_engine.search(q)

    ids = [r["doc_id"] for r in results]
    docs = get_docs_by_id(ids)

    for r in results:
        doc = docs.get(r["doc_id"])
        if doc:
            final_results.append({
                "id": r["doc_id"],
                "title": doc["title"].replace("_", " "),
                "url": doc["url"],
                "score": round(r["score"] * 100, 1)
            })
            
    return {
        "query": q,
        "result": final_results
    }
    
@app.get("/search")
async def get_results():
    return final_results

    
@app.delete("/search")
async def reset_results():
    final_results.clear()
    return {"message": "results cleared"}