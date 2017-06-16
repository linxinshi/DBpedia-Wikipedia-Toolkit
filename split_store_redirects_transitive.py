import sys
import pymongo
import string
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer

def findTitle(line):
    pos_head = line.find("resource/")
    pos_tail = -1
    return line[pos_head+9:pos_tail]
    
def main():
    rec_redirect={}
    src=open('redirects_transitive_en.nt','r')
    for line in src.readlines():
        l=line.strip().split(' ')
        if len(l)<3:
           continue
           
        h=findTitle(l[0].strip())
        t=findTitle(l[2].strip())
        
        if rec_redirect.has_key(t)==False:
           rec_redirect[t]=[]
        rec_redirect[t].append(h)
    src.close()

    # connect to the database
    client = pymongo.MongoClient("localhost",27017)
    db = client.test
    table_connection=db['redirect_transitive']
    
    cnt_batch=0
    batch=[]
    for t in rec_redirect:
        str='|'.join(rec_redirect[t])
        item={'title':t,'be_redirected_list':str}
        
        batch.append(item)
        cnt_batch+=1
        if cnt_batch==8000:
           item_id = table_connection.insert_many(batch)
           cnt_batch=0
           del batch[:]

    # process remaining record
    if cnt_batch>0:
       item_id = table_connection.insert_many(batch)
       cnt_batch=0
       del batch[:]

if __name__ == '__main__':
   reload(sys)
   sys.setdefaultencoding('utf-8')
   main()