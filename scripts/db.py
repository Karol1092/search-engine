import sqlite3

def get_docs_by_id(ids):
    conn = sqlite3.connect("data/articles.db")
    cur = conn.cursor()
    
    placeholders = ",".join(["?"] * len(ids))
    query = f"SELECT id, title, url FROM articles WHERE id in ({placeholders})"
    cur.execute(query, ids)
    
    rows = cur.fetchall()
    conn.close()
    
    docs = {row[0] : {"title": row[1], "url": row[2]} for row in rows}
    
    return docs