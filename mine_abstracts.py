# Some code to mine abstracts to do interesting things with them.

from pymongo import MongoClient
from bson.code import Code
from bson.objectid import ObjectId
import logging

from sys import stdout
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

db = MongoClient('localhost',27017).eml_docs
# Mine abstracts
abstracts = []
for doc in db.all.find():
   try:
      abstracts.append(doc["dataset"]["abstract"][0])
   except KeyError:
      pass
   except TypeError:
      pass

documents = []

for i in range(len(abstracts)):
   if abstracts[i].__class__.__name__ == 'str':
      documents.append(abstracts[i])
   if abstracts[i].__class__.__name__ == 'unicode':
      documents.append(abstracts[i].encode("utf-8"))
   if abstracts[i].__class__.__name__ == 'list':
      if len(abstracts[i]) > 0:
         while abstracts[i].__class__.__name__ == 'list':
            abstracts[i] = abstracts[i][0]
            documents.append(abstracts[i])

for i in range(len(documents)):
   if documents[i].__class__.__name__ == 'unicode':
      documents[i]=documents[i].encode("utf-8")

for i in range(len(documents)):
   while documents[i].__class__.__name__ == 'list':
      if documents[i][0].__class__.__name__ == 'str':
         documents[i] = documents[i][0]
         break

# run several times
for doc in documents:
   if doc.__class.__name__ != 'str':
      documents.remove(doc)



class MyCorpus(object):
   def __iter__(self):
      for line in open('mycorpus.txt'):
         yield dictionary.doc2bow(line.lower().split())

# GENSIM
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models, similarities

# remove common words and tokenize
stoplist = set('for a of the and to in were along during are is gce-lter and-lter bes-lter bnz-lter cdr-lter cwt-lter fce-lter jrn-lter mcm-lter ntl-lter nwt-lter pie-lter vcr-lter'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
   for document in documents]

# remove words that appear only once
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once]
   for text in texts]

dictionary = corpora.Dictionary(texts)
dictionary.save('/Users/jaakko/Desktop/eml_lter_abstracts.dict') # store the dictionary, for future reference

new_doc = db.all.find_one()['dataset']['title']
new_vec = dictionary.doc2bow(new_doc.lower().split())
print new_vec

corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('/Users/jaakko/Desktop/eml_lter_abstracts.mm', corpus) # store to disk, for later use
print corpus

# Create the TF-IDF model of the corpus
tfidf = models.TfidfModel(corpus)
#Create the LSI model behind the tf-idf

lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=6) # initialize an LSI transformation
corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi

lsi.print_topics(6)
