# usage
command: python extract_label.py FILENAME

A label is actually the corresponding wikipedia article name of a DBpedia uri  
  
# input
DBpedia labels dataset (in ttl triplet format)  
# output
pair (DBpedia_uri, label) for each line in the ttl file, seperated by tab

# behaviour
by default results will be stored in a mongoDB collection
# parameters
Set DEBUG_MODE=True if you want to output result to the console  
Set MONGO_MODE=True if you want to store results into a mongoDB collection (requires pymongo package)  
# other
works fine with DBpedia 2015-10 english version
