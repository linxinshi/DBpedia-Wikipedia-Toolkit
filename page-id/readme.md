command: python extract_page_id.py FILENAME  
  
input: DBpedia page-id dataset (in ttl triplet format)   
output: pair (DBpedia_uri, page_id) for each line in the ttl file   

by default results will be stored in a mongoDB collection  
  
Set DEBUG_MODE=True if you want to output result to the console  
Set MONGO_MODE=True if you want to store results into a mongoDB collection  
  
works fine for DBpedia 2015-10  

