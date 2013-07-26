'''
    Author: Jaakko Lappalainen, 2013. email: jkk.lapp@gmail.com
'''
""" 
   Some primitives that use MR native framework from MongoDB to get some basic stats from the data. It generates data to plot histograms.
"""
# Get relative occurrence of tags inside 'tag' in 'collection'
def countTags(collection, tag):
   mapper = Code("function () {"
         "           for(var i in this"+tag+") {"
         "              if(this"+tag+".hasOwnProperty(i)){"
         "                 emit(i, 1);"
         "              }"
         "           }"
         "        }")
   nDocs = collection.count()
   reducer = Code("function (key, values) {"
         "           var total = 0;"
         "           for (var i = 0; i < values.length; i++) {"
         "              total += values[i];"
         "           }"
         "           return total;"
         "        }")
   if tag == '':
      tag = 'output'
   result = collection.map_reduce(mapper, reducer, tag)
   r = {}
   for doc in result.find():
      r[doc['_id']] = doc['value']
   return r   

def countRelativeOccurrenceTags(collection, tag):
   mapper = Code("function () {"
         "           for(var i in this"+tag+") {"
         "              if(this"+tag+".hasOwnProperty(i)){"
         "                 emit(i, 1);"
         "              }"
         "           }"
         "        }")
   nDocs = collection.count()
   reducer = Code("function (key, values) {"
         "           var total = 0;"
         "           for (var i = 0; i < values.length; i++) {"
         "              total += values[i];"
         "           }"
         "           return total;"
         "        }")
   if tag == '':
      tag = 'output'
   result = collection.map_reduce(mapper, reducer, tag)
   r = {}
   nDocs = collection.count()
   for doc in result.find():
      n = float(doc['value'])/float(nDocs)*100
      r[doc['_id']] = n
   return r      

def countTagValues(collection, tag):
   mapper = Code("function () {"
         "           for(var i in this"+tag+") {"
         "               if(this"+tag+".hasOwnProperty(i)){"
         "                    emit(this"+tag+", 1);"
         "               }"
         "           }"
         "        }")
   reducer = Code('function (key, values) {'
         '           var total = 0;'
         '           if(key != "_id"){'
         '              for (var i = 0; i < values.length; i++) {'
         '                 total += values[i];'
         '              }'
         '           }'
         '           return total;'
         '        }')
   if tag == '':
      tag = 'output'
   result = collection.map_reduce(mapper, reducer, tag)
   nDocs = collection.count()
   r = {}
   for doc in result.find():
      n = float(doc['value'])/float(nDocs)*100
      r[doc['_id']] = "{0:.1f}".format(n)+" %"
   return r   

# Search for 'tag' in 'module'

def searchTag(collection, module, tag):
   mapper = Code("function () {"
         "           if(this"+module+".hasOwnProperty("+tag+")){"
         "                 emit(this"+module+"["+tag+"], 1);"
         "           }"
         "        }")
   nDocs = collection.count()
   reducer = Code("function (key, values) {"
         "           var total = 0;"
         "           for (var i = 0; i < values.length; i++) {"
         "              total += values[i];"
         "           }"
         "           return total;"
         "        }")
   if tag == '':
      tag = 'output'
   result = collection.map_reduce(mapper, reducer, tag)
   for doc in result.find():
      n = float(doc['value'])/float(nDocs)*100
      print (doc['_id']+" "+"{0:.1f}".format(n)+" %")

# Make a list with all the relevant tags inside a tag, using map-reduce

def listTags(col, tag):
   mapper = Code("function () {"
         "           for(var i in this"+tag+") {"
         "               if(this"+tag+".hasOwnProperty(i)){"
         "                    emit(i, 1);"
         "               }"
         "           }"
         "        }")
   reducer = Code("function (key, values) {"
         "           var total = 0;"
         "           for (var i = 0; i < values.length; i++) {"
         "              total += values[i];"
         "           }"
         "           return total;"
         "        }")
   if tag == '':
      tag = 'output'
   result = col.map_reduce(mapper, reducer, tag)
   k = []
   for doc in result.find():
      k.append(doc['_id'].encode("utf8"))
   return k

# Fields with longest text
def printLongestText(collection, tag):
   mapper = Code("function () {"
      "           length = 0;"
      "           for(var i in this"+tag+") {"
      "              if(this"+tag+".hasOwnProperty(i)){"
      "                 if(i.length > length){"
      "                    length = i.length;"
      "                 }"
      "              }"
      "           }"
      "           emit(i, length);"
      "        }")
   nDocs = collection.count()
   reducer = Code("function (key, values) {"
      "           var total = 0;"
      "           for (var i = 0; i < values.length; i++) {"
      "              total += values[i];"
      "           }"
      "           return total;"
      "        }")
   if tag == '':
      tag = 'output'
   result = collection.map_reduce(mapper, reducer, tag)
   for doc in result.find():
      print (doc['_id']+" "+"{0:.0f}".format(doc['value']))

def getTitleFromId(id):
   if id != "":
      return db.eml_docs.find({"_id": id})['dataset']['title']


def getAbsoluteOccurrences(collection, tag):
   mapper = Code("function () {"
         "           for(var i in this"+tag+") {"
         "              if(this"+tag+".hasOwnProperty(i)){"
         "                 emit(i, 1);"
         "              }"
         "           }"
         "        }")
   reducer = Code("function (key, values) {"
         "           var total = 0;"
         "           for (var i = 0; i < values.length; i++) {"
         "              total += values[i];"
         "           }"
         "           return total;"
         "        }")
   if tag == '':
      tag = 'output'
   result = collection.map_reduce(mapper, reducer, tag)
   data = {}
   for doc in result.find():
      data[doc['_id'].encode("utf8")] = doc['value']
   return data   
                           