import sys
import string

DEBUG_MODE=True
MONGO_MODE=False

if MONGO_MODE==True:
   import pymongo
    
def main():
    if len(sys.argv)<2:
       print 'error: too few arguments'
       print 'command:  python extract_mapping_based_property_object.py FILENAME'
       quit()

    # create mongoDB connection
    if MONGO_MODE==True:
       client = pymongo.MongoClient("localhost",27017)
       db = client.wiki2015
       table_connection=db['mapping_based_properties_object']   
       bulk = table_connection.initialize_ordered_bulk_op()
    
    # create file object
    filename=sys.argv[1]
    print 'processing '+filename
    
    with open(filename,'r') as src:
         lines=src.readlines()
         
         for line in lines:
             if line.startswith('#')==True:
                continue
                
             list_item=line.strip().split()
             uri=list_item[0]
             property=list_item[1]
             value=list_item[2]
            
             if DEBUG_MODE==True:
                print '%s\t%s\t%s'%(uri,property,value)
             if MONGO_MODE==True:
                bulk.insert({'uri':uri,'property':property,'value':value})
                
         if MONGO_MODE==True:
            bulk.execute()
            
    if MONGO_MODE==True:
       client.close()

if __name__ == '__main__':
   reload(sys)
   sys.setdefaultencoding('utf-8')
   main()
