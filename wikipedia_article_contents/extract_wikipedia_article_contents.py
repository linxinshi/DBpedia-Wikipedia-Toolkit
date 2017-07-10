import sys
import string
from gensim.corpora.wikicorpus import *

DEBUG_MODE=False
MONGO_MODE=True

if MONGO_MODE==True:
   import pymongo

def main():
    if len(sys.argv)<2:
       print 'error: too few arguments'
       print 'command:  python extract_wikipedia_article_content.py FILENAME'
       quit()

    # create mongoDB connection
    if MONGO_MODE==True:
       client = pymongo.MongoClient("localhost",27017)
       db = client.wiki2015
       table_connection=db['wiki_article_contents']   
       bulk = table_connection.initialize_ordered_bulk_op()
    
    # create file object
    filename=sys.argv[1]
    print 'processing '+filename
    
    with open(filename,'r') as src:
         for page_pair in extract_pages(src):
             label,content,page_id=page_pair[0],page_pair[1],page_pair[2]
             
             pair_tokens=process_article((content,False,label,page_id))
             content=' '.join(pair_tokens[0])
             
             if DEBUG_MODE==True:
                print '%s\t%s\t%s'%(label,page_id,content.encode('GBK', 'ignore'))
             if MONGO_MODE==True:
                bulk.insert({'label':label,'id':page_id,'content':content})
                
         if MONGO_MODE==True:
            bulk.execute()
            
    if MONGO_MODE==True:
       client.close()

if __name__ == '__main__':
   reload(sys)
   sys.setdefaultencoding('utf-8')
   main()
