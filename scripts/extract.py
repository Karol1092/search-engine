import mwxml
import mwparserfromhell
import re
import sqlite3

def main():
    dump = mwxml.Dump.from_file(open("data/simplewiki-latest-pages-articles.xml", "r", encoding="utf-8"))

    results = []

    for i, page in enumerate(dump):
        if i % 10000 == 0:
            print(f"step {i}")
            
        if page.namespace != 0:
            continue
        
        last_revision = None
        for revision in page:
            last_revision = revision
            
        if last_revision:
            title = page.title.replace(" ", "_")
            
            url = make_url(title)
            
            text = clear_wikitext(last_revision.text)
            text = remove_wiki_markers(text)
            text = post_process(text)   

            if len(text) < 150:
                continue
            
            results.append((title, text, url))
            
    print(f"Number of articles: {len(results)}")
    
    create_and_write_to_db(results)
    
    print("done.")


def clear_wikitext(wikitext):
    if not wikitext:
        return ""
    
    parsed = mwparserfromhell.parse(wikitext)
    
    text = parsed.strip_code(
        normalize=True,
        collapse=True
    )
    
    return text


def post_process(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\[[^\]]*\]", "", text)
    text.strip()
    return text

def remove_wiki_markers(text): 
    text = re.sub(r"\b\d+px\|\b", "", text)
    text = re.sub(r"\b(thumb\||left\||right\||frame\||center\|)\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\bcategory:\b", "", text, flags=re.IGNORECASE)
    return text

def make_url(title):
    return "https://simple.wikipedia.org/wiki/" + title

def create_and_write_to_db(to_insert):
    conn = sqlite3.connect("data/articles.db")
    cursor = conn.cursor()
    
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            text TEXT,
            url TEXT
        )
        """
    )
    conn.commit()
    
    cursor.executemany(
        "INSERT INTO articles (title, text, url) VALUES (?, ?, ?)",
        to_insert
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()