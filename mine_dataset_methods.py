'''
    Author: Jaakko Lappalainen, 2013. email: jkk.lapp@gmail.com
'''
''' Some code to mine the 'eml-methods' module. '''

for doc in col.find():
	try:
		method = doc['dataset']['methods']
		if method.__class__.__name__ == 'dict':
			if method['methodStep'][0].__class__.__name__ == 'list':
				if method['methodStep'][0][0].__class__.__name__ == 'dict':
					print method['methodStep'][0][0].keys()
				if method['methodStep'][0][0].__class__.__name__ == 'list':
					print method['methodStep'][0][0][0].__class__.__name__
			if method['methodStep'][0].__class__.__name__ == 'dict':	
				print method['methodStep'][0].keys()
		#if method.__class__.__name__ == 'list':
			#print method
	except KeyError:
		pass


types = []
for doc in col.find():
	try:
		d = doc['dataset']['methods']
		t = d.__class__.__name__
		if t not in types:
			types.append(t)
		if t == 'list':
			for element in d:
				x = t+":"+element.__class__.__name__
				if x not in types:
					types.append(x)
		if t == 'dict':

	except KeyError:
		pass


def flatList(list):
	if list.__class__.__name__ == 'list' and len(list) > 0:
		return flatList(list[0])
	else:
		return list


def flattenMethods(col):
	r = {}
	for doc in col.find():
		try:
			r[doc['_id']]=flatList(doc['dataset']['methods'])
			print r[doc['_id']].__class__.__name__
		except KeyError:
			pass
	return r

r = flattenMethods(col)

t = {}
for key in r.keys():
	method = r[key]
	if method.__class__.__name__ != 'list':
		t[key]=r[key]

for key in t.keys():
	method = t[key]
	if method.__class__.__name__ != 'unicode':
		try:
			print method['methodStep'][0][0]
		except KeyError:
			pass
