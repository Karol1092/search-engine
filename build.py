from scripts import download_dump, extract, make_matrix, make_LSA

def run_all():
    print("1. Wikipedia dump...")
    download_dump.main()
    
    print("2. Processing dump...")
    extract.main()
    
    print("3. TF-IDF...")
    make_matrix.main()
    
    print("4. LSA...")
    make_LSA.main()
    
    print("DONE")
    
    
if __name__ == "__main__":
    run_all()