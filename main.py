from pymongo import MongoClient
from bson.code import Code
from bson.objectid import ObjectId
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

db = MongoClient('localhost',27017)
col = db.eml_docs.all

# Count docs in collections
total = 0
for col in db.eml_docs.collection_names():
   if col != 'system.indexes':
      if col != 'all':
         print db.eml_docs[col].count()
         total+=db.eml_docs[col].count()


# Count metadata elements - not interesting
"""
mapper = Code(    "function () {"
               "  for(var i in this) {"
               "    if(this.hasOwnProperty(i)){"
               "      emit(i, 1);"
               "    }"
               "   }"
               "}")

reducer = Code("function (key, values) {"
            "       var total = 0;"
            "      for (var i = 0; i < values.length; i++) {"
            "        total += values[i];"
            "      }"
            "     return total;"
            "   }")
                
result = db.eml_docs.map_reduce(mapper, reducer, "MROutput")

for doc in result.find():
    print doc
"""



# Get tags absolute occurrences in a numpy array

import numpy as np

data = getAbsoluteOccurrences(col, '["dataset"]')

def rawDataFromDict(data):
   l = []
   for v in data.keys():
      l.append(data[v])
   return l

array = np.array(rawDataFromDict(data)).astype(int)

import matplotlib.pyplot as plt

plt.bar(range(0,array.size), array)

plt.figure().addsubplot(2,1,1).set_xticklabels(data.keys(),rotation=90, rotation_mode="anchor", ha="right")
plt.show()



# Check if doc['dataset']['access'] is the same as doc['access']
k = 0
j = 0
for doc in col.find():
   try:
      print "doc['access']: "+str(doc['access'])
      k+=1
   except KeyError:
      pass
   else:
      try:
         print "doc['dataset']['access']: "+str(doc['dataset']['access'])
         j+=1
      except KeyError:
         pass

print str(k)+", "+str(j)


for doc in col.find():
   try:
      print doc['access']
   except KeyError:
      pass
   else:
      break



printLongestText(col, '["dataset"]')

# Plot collection count by LTER site

import matplotlib.pyplot as plt

data = {}

for c in db.eml_docs.collection_names():
   if c != 'system.indexes':
      col = db.eml_docs[str(c)]
      data[str(c).replace("knb_lter_","")] = col.count()





import numpy as np

array = np.array(rawDataFromDict(data)).astype(int)


import matplotlib.pyplot as plt

ax = plt.subplot(111)
width=0.7
bins = map(lambda x: x-width/2,range(0,len(data)))
ax.bar(bins,array,width=width)
ax.set_xticks(map(lambda x: x, range(0,len(data))))
ax.set_xticklabels(data.keys(),rotation=0, ha="center")

plt.show()

