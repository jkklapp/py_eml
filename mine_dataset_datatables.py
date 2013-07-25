# Some scripts to mine data from 'dataTable' section in 'dataset'.

# Get datatables	
dt = {}
for doc in col.find():
	try:
		dt[doc['_id']] = doc['dataset']['dataTable']
	except KeysError:
		pass

# Analyze structure 
x = 100000
types = []
for key in dt.keys():
	if dt[key].__class__.__name__ == 'list':
		if len(dt[key][0].keys()) < x:
			x = len(dt[key][0].keys())
		print dt[key][0].keys()
	if dt[key].__class__.__name__ == 'dict':
		if len(dt[key].keys()) < x:
			x = len(dt[key].keys())
		print dt[key].keys()

# Get minimum set of common tags
common_tags = []
for key in dt.keys():
	doc = dt[key]
	if doc.__class__.__name__ == 'list':
		doc = doc[0]
	if len(doc.keys()) == 3:
		common_tags = doc.keys()

# Check that all docs have 'common_tags' tags
for key in dt.keys():
	doc = dt[key]
	if doc.__class__.__name__ == 'list':
		doc = doc[0]
	for subkey in common_tags:
		if subkey not in doc.keys():
			print doc.keys()
			break

# DESTROY LISTS!!!!
for key in dt.keys():
	doc = dt[key]
	if doc.__class__.__name__ == 'list':
		dt[key] = doc[0]

# Take a look at 'entityName's
for key in dt.keys():
	doc = dt[key]
	print doc['entityName']

# Not very useful

# Take a look at 'attributeList's
for key in dt.keys():
	doc = dt[key]
	print doc['attributeList']

# Take a look at 'physical'	
for key in dt.keys():
	doc = dt[key]
	print doc['physical']


# So, all docs have at least 'entityName', 'attributeList', and 'physical'. Lets group by similarity using genSim
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models, similarities

#From 'dt' to documents
documents = []
for key in dt.keys():
	documents.append(dt[key])

for doc in documents:
	if doc.__class__.__name__ == 'dict':
		print doc['physical']

