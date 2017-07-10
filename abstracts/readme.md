command: python extract_label.py FILENAME  
  
input: DBpedia abstracts (long abstracts or short abstracts) dataset (in ttl triplet format)  
output: pair (DBpedia_uri, abstract) for each line in the ttl file, seperated by tab  
  
by default results will be stored in a mongoDB collection  
  
Set DEBUG_MODE=True if you want to output result to the console  
Set MONGO_MODE=True if you want to store results into a mongoDB collection (requires pymongo package)  
  
works fine with DBpedia 2015-10 english version
