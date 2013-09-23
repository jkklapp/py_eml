'''
    Author: Jaakko Lappalainen, 2013. email: jkk.lapp@gmail.com
'''
''' Some scripts to mine data. Just select the tag you are interested in and 
the code counts the ocurrences. '''


####### Gets values from key in a json recursively
import json
def get_all(myjson, key,  result=None):
	result = [] if result is None else result
	if type(myjson) in (str,unicode):
		myjson = json.loads(myjson)
	if type(myjson) is dict:
		for jsonkey in myjson.keys():
			if type(myjson[jsonkey]) in (list, dict):
				get_all(myjson[jsonkey], key, result)
			elif jsonkey == key:
				result.append(myjson[jsonkey])
	elif type(myjson) is list:
		for item in myjson:
			if type(item) in (list, dict):
				get_all(item, key, result)

############################################

# common 'attributeName'-s
rawdata = []
for d in db.all.find():
	get_all(d,'dataset',rawdata)

data = {}
for d in rawdata:
	try:
		data[d]+=1
	except:
		data[d]=1

rawdata=data

for d in rawdata.keys():
	if rawdata[d] < 10:
		del rawdata[d]
		
names = rawdata.keys()
data = np.array(rawdata.values())
ax = plt.subplot(111)
width=1
bins = map(lambda x: x-width/2,range(1,len(data)+1))
ax.bar(bins,data,width=width)
ax.set_xticks(map(lambda x: x, range(1,len(data)+1)))
ax.set_xticklabels(names,rotation=90, rotation_mode="anchor", ha="right")
plt.show()
