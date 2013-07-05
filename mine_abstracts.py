from pymongo import MongoClient
from bson.code import Code
from bson.objectid import ObjectId
import logging

from sys import stdout
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

db = MongoClient('localhost',27017).eml_docs
# Mine abstracts
abstracts = []
for doc in db.eml_docs.find():
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



for doc in documents:
   if doc.__class__.__name__ != 'list':
      print doc[0].__class__.__name__
      break

for doc in abstracts:
   if doc.__class__.__name__ == 'dict':
      try:
         print doc['para']         
      except KeyError:         
         pass

def returnSimilarWords(word):
   for i in dictionary:
      j = len(word) 
      while j > 0:
         w



