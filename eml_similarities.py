from pymongo import MongoClient
import simplejson
from gensim import corpora, models, similarities
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# Open a connection
client = MongoClient('localhost',27017)
# Retrieve de DB
db = client.eml_docs
# Get the collection
eml_docs = db.eml_docs
# Predefined dictionary - from OE keyword set
dictionary = corpora.Dictionary.load('/home/jaakko/dict.d')

def FindKeys(s):
    return [dictionary[keyword] for keyword in dictionary if dictionary[keyword]
        in s and dictionary[keyword] is not '']

# Create a corpus with the titles
class CreateCorpus(object):
     def __iter__(self):
         for doc in eml_docs.find({}, fields={ u'dataset' : True, u'title' : True }):
             yield dictionary.doc2bow(FindKeys(doc))
 
# Build the corpus                    
title_corpus = CreateCorpus()
# Run distributed LSA on nine documents
lsi = models.LsiModel(title_corpus, id2word=dictionary, num_topics=200, chunksize=1, distributed=True)

########## GetDatasetFields ################
def getDatasetFields(field):
    list_of_docs = eml_docs.find({}, fields={ u'dataset' : True, u'title' : True})
    for i in range(list_of_docs.count()):
        print list_of_docs[i]['dataset'].get(field)
        
############### DICTIONARY #################
# Create a dictionary
for key in getDatasetFields('keywordSet'):
    dictionary = corpora.Dictionary(key.lower().split('\n')) 
####################################################################################################        
        
for doc in eml_docs.find():   
    dictionary = corpora.Dictionary(simplejson.loads(doc)['title'].lower().split('\n'))
        
        
dictionary = corpora.Dictionary(simplejson.loads(doc)['title'].lower().split('\n'))
    for doc in eml_docs.find()
       
parsed_data = simplejson.loads(line)['title'] parsed_data['title']
