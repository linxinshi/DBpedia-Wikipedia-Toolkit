import sys
import pymongo
import string
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer

def cleanSentence(line,isLower=True):
    if len(line)==0:
       return ''

    replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
    #line=str(line).translate(replace_punctuation).lower()      
    try:
       line = line.encode('utf-8').translate(replace_punctuation)
       if isLower==True:
          line=line.lower()
    except Exception,e:
       print 'encode error'
       return line
    line=' '.join(line.split())
    return line.decode('utf-8')

def cleanRelation(line):
    # http:
    l=re.findall('[a-zA-Z][^A-Z]*',line)
    return ' '.join(l)
    
def cleanValue(line):
    # value or http:
    if line.find('http')!=-1:
       pos_head = line.find("resource/")+9
       return line[pos_head:]
    else:
       return line
    
def cleanDBpediaValue(line):
    # relation%%%%value$$$$relation%%%%value
    if len(line)==0:
       return ''
    l=line.split('$$$$')
    res=''
    for item in l:
        pair=item.split('%%%%') # relation value
        relation=pair[0]
        value=pair[1]
        res=res+'%s %s '%(cleanRelation(relation),cleanValue(value))
    return cleanSentence(res,True)

def stemSentence(line,stemmer=SnowballStemmer('english'),isCleanNeeded=True):
    if isCleanNeeded==True:
       line=cleanSentence(line,True)
    if stemmer is None:
       stemmer=SnowballStemmer('english')
    list=line.split(' ')
    stemlist=[stemmer.stem(word) for word in list]
    res=' '.join(stemlist)
    return res

def remove_duplicate(line):
    ltmp=line.split(' ')
    l=list(set(ltmp))
    l.sort(key=ltmp.index)
    res=' '.join(l)
    return res

def findName(line):
    res_temp = findRawName(line)
    res_str=''
    pos_head=0
    
    #print "now name="+res_temp	
    for pos_head in range(len(res_temp)-1):
        if res_temp[pos_head]=='(' or res_temp[pos_head]==')':
           continue
        elif res_temp[pos_head]=='_':
           res_str=res_str+" "
        elif res_temp[pos_head].islower() and res_temp[pos_head+1].isupper():
           res_str=res_str+res_temp[pos_head]+" "
        else:
           res_str=res_str+res_temp[pos_head]
    if len(res_temp)>0:
       if res_temp[-1] not in ['(',')','_']:
          res_str=res_str+res_temp[-1]
    
    return cleanSentence(res_str)
    
def findTitle(line):
    pos_head = line.find("resource/")
    pos_tail = -1
    return line[pos_head+9:pos_tail]
    
def findID(line):
    #print 'raw id ='+line
    pos_head=line.find('?oldid=')
    pos_tail=-1
    return line[pos_head+7:pos_tail]
    
def findRelation(line):
    return line.strip()[1:-1]
    
def findValue(line):
    # find quote , quote means value is a string identifier , otherwise it will be an uri
    flag_quote = line.find('\"') 
    if flag_quote > -1:
       pos_head = 1
       pos_tail = line.rfind('\"')
    else:
       pos_head = line.find("resource/")+9
       pos_tail = -1
    return line[pos_head:pos_tail]

def findType(line):
    # find quote , quote means value is a string identifier , otherwise it will be an uri
    #print 'line=%s'%(line)
    list_item=line.split('^^')
    if len(list_item)<2:
       return ''
    else:
       return list_item[1][1:-1]
    
# ===========================================================================


def main():

    # read from dbpedia
    src_dbpedia=open('mappingbased_properties_cleaned_en.nq','r')
    #src_dbpedia=open('debug.txt','r')
    lines=src_dbpedia.readlines()
    src_dbpedia.close()
    
    type_sample_value={}
    
    for line_src in lines:
        if cmp(line_src,'# completed') == 0:
           break
        if len(line_src) == 0:
           break
        # first line
        if line_src[0] == '#':
           continue
        
        list_db = line_src.strip('.').strip().split('>')
        list_db[0]=list_db[0].strip()+'>'
        list_db[1]=list_db[1].strip()+'>'
        list_db[2]=list_db[2].strip()+'>'
        # list_db[2] has two situation
        title= findTitle(list_db[0])
        relation = findRelation(list_db[1])
        value = findValue(list_db[2])
        type = findType(list_db[2])

        if len(type.strip())==0:
           continue
           
        if type_sample_value.has_key(type)==False:
           type_sample_value[type]=[]
           
        if len(type_sample_value[type])<3:
           type_sample_value[type].append(value)
        
        #assert unicode(type_relation[relation])==unicode(type)
        #if type_relation[relation]!=type:
            #print 'relation=%s  type=%s   %s'%(relation,type,type_relation[relation])
            #break
    
    for type in type_sample_value:
        str_value=' '.join(type_sample_value[type])
        print '%s\t%s'%(type,str_value)        
    
if __name__ == '__main__':
   reload(sys)
   sys.setdefaultencoding('utf-8')
   main()