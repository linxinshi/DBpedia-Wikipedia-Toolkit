import sys
import string

DEBUG_MODE=False
MONGO_MODE=True

if MONGO_MODE==True:
   import pymongo

def extractID(line):
    h=line.find('"')
    t=line.rfind('"')
    if h==-1 or t==-1:
       return '-1'
    else:
       return line[h+1:t]

def main():
    if len(sys.argv)<2:
       print 'error: too few arguments'
       print 'command:  python extract_label.py FILENAME'
       quit()

    # create mongoDB connection
    if MONGO_MODE==True:
       client = pymongo.MongoClient("localhost",27017)
       db = client.wiki2015
       table_connection=db['label']   
       bulk = table_connection.initialize_ordered_bulk_op()
    
    # create file object
    filename=sys.argv[1]
    print 'processing '+filename
    
    with open(filename,'r') as src:
         lines=src.readlines()
         
         for line in lines:
             if line.startswith('#')==True:
                continue
                
             list_item=line.strip().split('>')
             dbpedia_uri=list_item[0]+'>'
             label=extractID(list_item[2].strip())
             
             if DEBUG_MODE==True:
                print '%s\t%s'%(dbpedia_uri,label)
             if MONGO_MODE==True:
                bulk.insert({'uri':dbpedia_uri,'label':label})
                
         if MONGO_MODE==True:
            bulk.execute()
            
    if MONGO_MODE==True:
       client.close()

if __name__ == '__main__':
   reload(sys)
   sys.setdefaultencoding('utf-8')
   main()
