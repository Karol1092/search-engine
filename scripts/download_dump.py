import os
import requests
import bz2

dump_url = "https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-pages-articles.xml.bz2"
input_path = "data/wiki.xml.bz2"
output_path = "data/wiki.xml"

def main():
    os.makedirs("data", exist_ok=True)
    
    print("Downloading...")
    
    with requests.get(dump_url, stream=True) as r:
        r.raise_for_status()
        with open(input_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
                    
    print("Extracting...")
    
    with bz2.open(input_path, "rb") as f_in:
        with open(output_path, "wb") as f_out:
            for chunk in iter(lambda: f_in.read(1024 * 1024), b""):
                f_out.write(chunk)
    
if __name__ == "__main__":
    main()