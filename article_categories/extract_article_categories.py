import sys
import string

DEBUG_MODE=False
MONGO_MODE=True

if MONGO_MODE==True:
   import pymongo

def extractCategory(line):
    h=line.find('Category:')
    if h==-1:
       return '-1'
    else:
       return line[h+9:-1]

def main():
    if len(sys.argv)<2:
       print 'error: too few arguments'
       print 'command:  python extract_article_categories.py FILENAME'
       quit()

    # create mongoDB connection
    if MONGO_MODE==True:
       client = pymongo.MongoClient("localhost",27017)
       db = client.wiki2015
       table_connection=db['article_categories']   
       bulk = table_connection.initialize_ordered_bulk_op()
    
    # create file object
    filename=sys.argv[1]
    print 'processing '+filename
    
    with open(filename,'r') as src:
         lines=src.readlines()
         
         uri_cat={}
         for line in lines:
             if line.startswith('#')==True:
                continue
                
             list_item=line.strip().split()
             dbpedia_uri=list_item[0]
             category=extractCategory(list_item[2].strip())
             
             if uri_cat.has_key(dbpedia_uri)==False:
                uri_cat[dbpedia_uri]=[]
             uri_cat[dbpedia_uri].append(category)
        
         for uri in uri_cat:
             categories='|'.join(uri_cat[uri])
        
             if DEBUG_MODE==True:
                print '%s\t%s'%(uri,categories)
             if MONGO_MODE==True:
                bulk.insert({'uri':uri,'categories':categories})
                
         if MONGO_MODE==True:
            bulk.execute()
            
    if MONGO_MODE==True:
       client.close()

if __name__ == '__main__':
   reload(sys)
   sys.setdefaultencoding('utf-8')
   main()
