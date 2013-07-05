from pymongo import MongoClient
from bson.code import Code
#require "sinatra"
#require "rdf"
#require "sparql/client"
#require "sparql"
#require "uri"
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

db = MongoClient('localhost',27017).eml_docs

def cls(): print "\n" * 100


cls()

def getText(raw):
    while(raw.__class__.__name__ != 'unicode'):
        raw = raw[0]
    return raw

def listProjectFields(field):
    list = []
    for i in db.eml_docs.find():
        try:
            list.append([i['dataset']['project'][field], i['_id']]  )
            pass
        except KeyError:
            pass
    return list

def listGeographicDescription():
    list = []
    for i in db.eml_docs.find():
        try:
            list.append([i['dataset']['project']['studyAreaDescription'][0][0]['geographicDescription'],i['_id']])
            pass
        except KeyError:
            pass
    return list

def listAbstracts():
    list = []
    for i in db.eml_docs.find():
        try:
            list.append([i['dataset']['project']['abstract'][0][0],i['_id']])
            pass
        except KeyError:
            pass
    return list





# This mapper emits the value of each key on the document
summarizer = Code("function summarizer() {"
               "    for(var i in this['dataset']) {"
               "        var sum = require( 'sum' );"
               "        var summary = sum({ 'corpus': i });" 
               "        emit(summary, this['dataset']['title']);"
               "    }"
               "  }")

# Define the function for the nested map reduce.
#clusterize = Code("function clusterize(key, values) {"
#                "   return mapReduce(compare, countClusters, {'out': test})"
#                "  }")

# This reducer executes a summarizer for each value emitted. The summarization is done
# using map reduce.
#tagcomparator = Code("function (key, values) {"
#                "       var total = 0;"
#                "       for (var i = 0; i < values.length; i++) {"
#                "         clusterize(key,values);"
#                "       }"
#                "       return total;"
#                "     }")

# This mapper summarizes the input and emits the summary made with sum.js
#compareMap = Code ("function compare() {           "
#                "       var sum = require( 'sum' );"
#	            "       var abstract = sum({ 'corpus': this });"
#                "       emit(abstract, 1);"
#                "   }")

# This reducer counts the summarizations.
count = Code ("function (key, values) {"
              "     return values.length;"
              "}")
                
           
            
result = db.eml_docs.map_reduce(summarizer, count, "MROutput")

for doc in result.find():
    print doc