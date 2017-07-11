import sys
import string

DEBUG_MODE=True
MONGO_MODE=False

if MONGO_MODE==True:
   import pymongo

def extractValueAndType(line):
    pos=line.find('<')
    type='NONE'
    if pos>-1:
       type=line[pos:]+'>'
       line=line[:pos]
    h=line.find('"')
    t=line.rfind('"')
    if h==-1 or t==-1:
       return 'UNKNOWN_ERROR','NONE'
    else:
       return line[h+1:t].replace('\\"',' ').strip(),type
    
def main():
    if len(sys.argv)<2:
       print 'error: too few arguments'
       print 'command:  python extract_long_abstracts.py FILENAME'
       quit()

    # create mongoDB connection
    if MONGO_MODE==True:
       client = pymongo.MongoClient("localhost",27017)
       db = client.wiki2015
       table_connection=db['mapping_based_properties_literal']   
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
             uri=list_item[0]+'>'
             property=list_item[1]+'>'
             value,type=extractValueAndType(list_item[2].strip())
             
             if value=='UNKNOWN_ERROR':
                print 'error line:'+line
             
             if DEBUG_MODE==True:
                print '%s\t%s\t%s\t%s'%(uri,property,value,type)
             if MONGO_MODE==True:
                bulk.insert({'uri':uri,'property':property,'value':value,'value_type':type})
                
         if MONGO_MODE==True:
            bulk.execute()
            
    if MONGO_MODE==True:
       client.close()

if __name__ == '__main__':
   reload(sys)
   sys.setdefaultencoding('utf-8')
   main()
