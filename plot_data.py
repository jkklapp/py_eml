'''
    Author: Jaakko Lappalainen, 2013. email: jkk.lapp@gmail.com
'''
''' Prepare data to plot'''
tags = {}
for c in db.eml_docs.collection_names():
   if c != 'system.indexes':
      #if c == 'all':
      if c != "['dataset']":
         tags[str(c)]=countRelativeOccurrenceTags(db.eml_docs[str(c)], "['dataset']['methods']") 


try:
   del tags["['dataset']"]
except KeyError:
   pass

db.eml_docs["['dataset']"].drop()

for dict in tags:
   if '@id' in tags[dict].keys():
      del tags[dict]['@id']
   if '@system' in tags[dict].keys():
      del tags[dict]['@system']
   if '0' in tags[dict].keys():
      del tags[dict]['0']
   for i in range(0,15):
      if str(i) in tags[dict].keys():
         del tags[dict][str(i)]

# RUN TWICE!!!
c = 0
for dict in tags:
   if c < len(tags[dict].keys()):
      c = len(tags[dict].keys())
      x = tags[dict].keys()

for dict in tags:
   for key in x:
      if key not in tags[dict].keys():
         tags[dict][key] = 0

for dict in tags:
   print len(tags[dict].keys())
   print tags[dict].keys()

# Plot collection count by LTER site
import matplotlib.pyplot as plt
import numpy as np

def rawDataFromDict(data):
   l = []
   for v in data.keys():
      l.append(data[v])
   return l

data = {}

for c in db.eml_docs.collection_names():
   if c != 'system.indexes':
      if c != 'all':
         col = db.eml_docs[str(c)]
         data[str(c).replace("knb_lter_","")] = col.count()

k = []
v = []
for key in sorted(data.keys()):
   k.append(key)
   v.append(data[key])

array = np.array(v)

# Some functions to plot data. Basically histograms...

import matplotlib.pyplot as plt

ax = plt.subplot(111)
width=0.9
bins = map(lambda x: x-width/2,range(0,len(k)))
ax.bar(bins,array,width=width)
ax.set_xticks(map(lambda x: x, range(0,len(k))))
ax.set_xticklabels(k, rotation=0, ha="center")
plt.subplots_adjust(left = 0.22, right = 0.78, bottom = 0.75)
plt.gca().set_xlim([0, 26])
plt.savefig('all.png', dpi=200, transparent=True, bbox_inches='tight', pad_inches=0)



i=1
for dict in tags:
   d = tags[dict]
   k = []
   v = []
   for key in sorted(d):
      k.append(key)
      v.append(d[key])
   hf, ha = plt.subplots(3,2)
   ha[-1, -1].axis('off')   
   array = np.array(v)
   ax = plt.subplot(111)
   i+=1
   width=1
   bins = map(lambda x: x-width/2, range(0, len(v)))
   ax.bar(bins, array, width=width)
   #if dict.replace("knb_lter_","") == 'vcr' || :
   ax.set_xticks(map(lambda x: x-width/2, range(0, len(v))))
   ax.set_xticklabels(k, rotation='vertical', ha="left")
   #else:
   #ax.set_xticklabels([])
   #plt.suptitle(dict.replace("knb_lter_",""), fontsize=20)
   ax.text(1.15, 0.5, dict.replace("knb_lter_",""),
        horizontalalignment='center',
        transform=ax.transAxes)
   plt.subplots_adjust(left = 0.55, right = 0.78, bottom = 0.72)
   plt.gca().set_xlim([0, len(v)])
   plt.gca().set_ylim([0, 100])
   #mytitle = plt.suptitle(dict.replace("knb_lter_",""))
   plt.show()
   #plt.savefig('Desktop/methods/'+dict+'methods.png', dpi=200, transparent=True, bbox_inches='tight', pad_inches=0)
   break
