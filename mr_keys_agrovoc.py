# Build a set of tuples (id, keyWordSet, abstract)

from pymongo import MongoClient
from bson.code import Code
from bson.objectid import ObjectId
import logging
import re
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

db = MongoClient('localhost',27017).eml_docs
from topia.termextract import tag
tagger = tag.Tagger()
tagger.initialize()

def cleanTerms(terms):
    if terms == []:
        return []
    r = []
    for t in terms:
        t = t.replace("),","")
        t = t.replace(", ","")
        if t != '':
            r.append(t)
    return r

"""
Summarizer
"""

from collections import defaultdict
import re

MAX_SUMMARY_SIZE = 300


'''Very simple white space tokenizer, in real life we'll be much more
fancy.
'''


def tokenize(text):
    return tagger.tokenize(text)



'''
Very simple spliting to sentences by [.!?] and paragraphs.
In real life we'll be much more fancy.
'''


def split_to_sentences(text):
    sentences = []
    start = 0
    for match in re.finditer('(\s*[.!?]\s*)|(\n{2,})', text):
        sentences.append(text[start:match.end()].strip())
        start = match.end()
    if start < len(text):
        sentences.append(text[start:].strip())
    return sentences


'''Return frequency (count) for each token in the text'''


def token_frequency(text):
    frequencies = defaultdict(int)
    for token in tokenize(text):
        frequencies[token] += 1
    return frequencies



def sentence_score(sentence, frequencies):
    return sum((frequencies[token] for token in tokenize(sentence)))


def create_summary(sentences, max_length):
    summary = []
    size = 0
    for sentence in sentences:
        summary.append(sentence)
        size += len(sentence)
        if size >= max_length:
            break
    summary = summary[:max_length]
    return '\n'.join(summary)


def summarize(text, max_summary_size=MAX_SUMMARY_SIZE):
    frequencies = token_frequency(text)
    sentences = split_to_sentences(text)
    sentences.sort(key=lambda s: sentence_score(s, frequencies), reverse=1)
    summary = create_summary(sentences, max_summary_size)
    return summary



"""
---------------------------------------------------------------------------
"""

def isType(object, type):
    return object.__class__.__name__ == type



def parseListOfDictKeys(list):
    try:
        return parseListOfUnicodeKeys([list['keyword']])
    except KeyError:
        return parseListOfUnicodeKeys([list['#text']])



def parseListOfUnicodeKeys(list):
    r = []
    #while isType(list[0],'list'):
    #    list = list[0]
    if isType(list[0], 'dict'):
        try:
            list = list[0]['keyword']
        except KeyError:
            list = list[0]['#text']
    if len(list) > 1:        
        for term in list:
            r.append(term.encode("utf8"))
    else:
        r.append(list[0].encode("utf8"))
        try:
            r.remove(' ')
            r.remove('')
        except ValueError:
            pass
    return r


def parseListOfDictsKeys(list):
    r = []
    for dict in list:
        try:
            r.append(dict['#text'])
        except TypeError:
            r.append(dict[0]['#text'])
    return r


def getKeyFromDoc(doc):
    try:
        kSet = doc['dataset']['keywordSet'] 
        if isType(kSet, 'list') and isType(kSet[0], 'unicode'):
            return parseListOfUnicodeKeys(kSet)
        if isType(kSet, 'list') and isType(kSet[0], 'dict') and len(kSet) == 1:
            return parseListOfDictKeys(kSet[0])
        if isType(kSet, 'list') and isType(kSet[0], 'dict') and len(kSet) > 1:
            return parseListOfUnicodeKeys(parseListOfDictsKeys(kSet))
        if isType(kSet, 'dict'):
            return parseListOfDictKeys(kSet)
    except KeyError:
        pass


tuples = {}

#f = open('tuples', 'w')

for doc in db.eml_docs.find():
    try:
        title = doc['dataset']['title'].encode("utf8")
        abstract = doc["dataset"]["abstract"][0].encode("utf8")
        abstract = re.sub("\n","",abstract)
        title = re.sub("\n","",title)
        keys = getKeyFromDoc(doc)
        _id = str(doc['_id'])
        if len(tokenize(abstract)) > 50:
            abstract = summarize(abstract, 1)
    except KeyError:
        pass
    except TypeError:
        pass
    except AttributeError:
        pass
    else:
        if keys.__class__.__name__ != 'NoneType':
            tuples[_id] = [title, abstract, keys]


from topia.termextract import extract
extractor = extract.TermExtractor(tagger)
extractor.filter = extract.DefaultFilter(singleStrengthMinOccur=2)
#extractor.filter = extract.permissiveFilter

extracted_dict = {}

for _id in tuples.keys():
    extracted_dict[_id] = []
    for term in extractor(tuples[_id][1]):
        if term != '':    
            extracted_dict[_id].append(term[0])


sets_to_compare = []
for _id in tuples.keys():
    sets_to_compare.append([_id, tuples[_id][2], extracted_dict[_id]])

from difflib import SequenceMatcher

def evalSimilarity(s1, s2):
    m = SequenceMatcher(None, s1, s2)
    return m.ratio()

"""
keyword set comparison
"""

for doc in sets_to_compare:
    try:
        print str(doc[1])+", "+str(doc[2])+" -> "+str(evalSimilarity(str(doc[1][0]), str(doc[2][0])))
    except IndexError:
        print doc
        break


"""

temp = {}

for _id in extracted_dict:
    temp[_id] = cleanTerms(extracted_dict[_id])

extracted_dict = temp







for tuple in tuples:
	f = open('/home/hduser/kea-5.0_full/temp/'+tuple+'.txt', 'w')
	f.write(tuples[tuple][1])
	f.close()

import commands
status, output = commands.getstatusoutput("java -classpath /home/hduser/kea-5.0_full/bin:/home/hduser/kea-5.0_full/bin:/home/hduser/kea-5.0_full/bin/kea:/home/hduser/kea-5.0_full:/home/hduser/kea-5.0_full/lib/commons-logging.jar:/home/hduser/kea-5.0_full/lib/icu4j_3_4.jar:/home/hduser/kea-5.0_full/lib/iri.jar:/home/hduser/kea-5.0_full/lib/jena.jar:/home/hduser/kea-5.0_full/lib/snowball.jar:/home/hduser/kea-5.0_full/lib/weka.jar:/home/hduser/kea-5.0_full/lib/xercesImpl.jar:/home/hduser/kea-5.0_full/lib/kea-5.0.jar:/home/hduser/kea-5.0_full:/home/hduser/kea-5.0_full/lib/commons-logging.jar:/home/hduser/kea-5.0_full/lib/icu4j_3_4.jar:/home/hduser/kea-5.0_full/lib/iri.jar:/home/hduser/kea-5.0_full/lib/jena.jar:/home/hduser/kea-5.0_full/lib/snowball.jar:/home/hduser/kea-5.0_full/lib/weka.jar:/home/hduser/kea-5.0_full/lib/xercesImpl.jar:/home/hduser/kea-5.0_full/lib/kea-5.0.jar kea.main.KEAKeyphraseExtractor -l /home/hduser/kea-5.0_full/temp -m /home/hduser/kea-5.0_full/FAO-20docs -v agrovoc -f skos")

print output

import os

for file in os.listdir("temp"):
    _id = f.name
    _id = re.sub(".txt","",_id)
    try:
        f = open("temp/"+file+".key", 'r')
    except IOError:
        pass
    _id = re.sub("temp/","",_id)
    t = f.readline()
    s = f.readline()
    while s:
        t +=", "+s
        s = f.readline()
    extracted_dict[_id] = t
"""

"""

"""""""

keys = []
for doc in db.eml_docs.find():
    try:
        keys.append(doc['dataset']['keywordSet'])
    except KeyError:
        pass


""""""
    Work with list of unicode elements
""""""

key_list_unicode = []
for doc in keys:
     if doc.__class__.__name__ == 'list':
             if doc[0].__class__.__name__ == 'unicode':
                     key_list_unicode.append(doc)



""""""""""""""""""""""""""""""""""""""""""

""""""
    Dictionary of keys
""""""
key_dict = []
for doc in keys:
    if doc.__class__.__name__ == 'dict':
        key_dict.append(doc)
    if doc.__class__.__name__ == 'list':
        if doc[0].__class__.__name__ == 'dict':
            key_dict.append(doc[0])

clean_key_dict = []

for doc in key_dict:
    try:
        clean_key_dict.append(doc['#text'].split(','))
    except KeyError:
        try:
            clean_key_dict.append(doc['keyword'])
        except KeyError:
            print doc
            break

for doc in clean_key_dict:
    if doc.__class__.__name__ != 'list':
        print doc
        break



""""""""""""""""""""""""""""""""""""""""""







test = []
for doc in key_list_dict:
    test.append(parseListOfDictKeys(doc))


""""""""""""""""""""""""""""""""""""""""""


r = []
for doc in db.eml_docs.find():
    try:
        r.append(getKeyFromDoc(doc))
    except KeyError:
        pass
"""


