# usage
python extract_wikipedia_article_contents.py FILENAME  
# package
gensim

# input
Wikipedia dump (enwiki-xxxx-pages-articles.xml)
# output
label(Wikipedia article title), page_id, content (seperated by tab)  
please notice punctuation,markup,templates in a Wikipedia article are removed

# behaviour
by default results will be stored into a mongoDB collection  
# parameters
set DEBUG_MODE=True if you want to output results to the console  
set MONGO_MODE=True if you want to store results into mongoDB
# notice
Wikipedia dump is huge, the program may consume a lot of computing resources
For Wikipedia dump 20151002 (English Version), the program takes about 55 hours.  If you only need content, WikiExtractor is recommended because it supports multiprocessing.
