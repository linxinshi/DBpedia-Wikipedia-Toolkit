command: python extract_article_categories.py FILENAME  
  
input: DBpedia labels dataset (in ttl triplet format)  
output: pair (DBpedia_uri, categories) for each line in the ttl file  
  
by default results will be stored in a mongoDB collection  
  
Set DEBUG_MODE=True if you want to output result to the console  
Set MONGO_MODE=True if you want to store results into a mongoDB collection (requires pymongo package)  
  
works fine for DBpedia 2015-10 english version  
  
SAMPLE OUTPUT(seperated by tab delimiter)  
<http://dbpedia.org/resource/Animalia_(book)>	Children's_picture_books|Alphabet_books|1986_books|Picture_books_by_Graeme_Base|Puzzle_books
