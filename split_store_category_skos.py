import sys
import pymongo
import string
from nltk.tokenize import word_tokenize

# ===========================================================================

def makeSentence(line):
    list_word = word_tokenize(line)
    res_str = ''
    for item_list in list_word:
        res_str = res_str + item_list + ' '
    return res_str

def cleanSentence(line):
    replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
    line=line.translate(replace_punctuation).lower()    
    line=' '.join(line.split())
    return line

def findRawName(line):
    flag_url = line.find("http")
    if flag_url > -1:
       pos_head = line.rfind('/')+1
       pos_tail = -1
    else:
       pos_head = 0
       pos_tail = -1
       
    return line[pos_head:pos_tail]

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

def findValue(line):
    flag_quote = line.find('\"')  # find quote
    if flag_quote > -1:
       pos_head = 1
       pos_tail = line.rfind('\"')
    else:
       pos_head = line.rfind('/')+1
       pos_tail = -1       

    res_temp = line[pos_head:pos_tail]
    '''
    if flag_quote > -1:
       res_str = makeSentence(res_temp)
    else:
       res_str = res_temp
       
    return cleanSentence(res_str)
    '''
    return cleanSentence(res_temp)
# ===========================================================================

reload(sys)
sys.setdefaultencoding('utf-8')

# connect to the database
client = pymongo.MongoClient("localhost",27017)
db = client.test
table_connection = db['skos_category']
#filename ='skos_category_sample.txt'
filename = 'skos_categories_en.nq'
src = open(filename,'r')

for line_src in src.readlines():
    line_src = line_src.strip()
    if cmp(line_src,'# completed') == 0:
       break
    if len(line_src) == 0:
       break
    # first line
    if line_src[0] == '#':
       continue
    
    raw_category='NONE'
    #list_item = line_src.split(' ')
    list_item = line_src.split('>')
    category_name = list_item[0].strip()+'>'
    
    #category_value = list_item[2].strip()
    if list_item[2].find('\"')>-1:
       # casual data number or string
       temp_list=list_item[2].split('<')
       category_value=temp_list[0] 
    else:
       # value is entity 
       category_value=list_item[2].strip()+'>'
       raw_category=findRawName(category_value)
       

    #print "raw value:"+category_value
    
    category_title = findRawName(category_name)
    category_name = findName(category_name)
    category_value=findValue(category_value)
    
    if category_value[0:9]=='category ':
       category_value=category_value[9:]
    if raw_category[0:9]=='Category:':
       raw_category=raw_category[9:]    
       
    # store into database
    
    try:
       item =  {"title":category_title,"name":category_name,"value":category_value,"raw_value":raw_category}
       item_id = table_connection.insert(item)
    except Exception,e:
       print "error"
    
    #print 'title='+category_title+'   name='+category_name+'  value='+category_value+'   raw_value:'+raw_category

client.close()    
src.close()

