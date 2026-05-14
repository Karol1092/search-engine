from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from search_engine import SearchEngine, TfidfBackend, LsaBackend
from db import get_docs_by_id

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

backends = {
    "tfidf": TfidfBackend(),
    "lsa": LsaBackend()
}

search_engine = SearchEngine(
    backends,
    default="tfidf",
    k=50
)

class SearchRequest(BaseModel):
    text: str

@app.post("/search")
async def search(q: SearchRequest):
    results = search_engine.search(q.text)

    ids = [r["doc_id"] for r in results]
    docs = get_docs_by_id(ids)
    
    final_results = []

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
        "query": q.text,
        "results": final_results
    }