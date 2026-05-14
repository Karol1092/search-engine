from scripts import extract, make_matrix, make_LSA

def run_all():
    print("1. Processing dump...")
    extract.main()
    
    print("2. TF-IDF...")
    make_matrix.main()
    
    print("3. LSA...")
    make_LSA.main()
    
    print("DONE")
    
    
if __name__ == "__main__":
    run_all()