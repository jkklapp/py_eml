'''
    Author: Jaakko Lappalainen, 2013. email: jkk.lapp@gmail.com
'''
'''
 This code implements the case study conducted on the paper. It tries to measure
 the time the experiment lasted vs the time that lasted until the publication 
 of the associated paper.
'''
###### Compare the number of days the exp. lasted vs publication date
expTimes = []
pubTimes = []

for doc in db.eml_docs['knb_lter_gce'].find():
   date_format = "%Y-%m-%d"        
   if doc['dataset']['coverage']['temporalCoverage'][0].__class__.__name__ == 'dict':
      beginDate = doc['dataset']['coverage']['temporalCoverage'][0]['beginDate'][0]
   if doc['dataset']['coverage']['temporalCoverage'][0].__class__.__name__ == 'list':
      beginDate = doc['dataset']['coverage']['temporalCoverage'][0][0]
   if doc['dataset']['coverage']['temporalCoverage'][0].__class__.__name__ == 'dict':
      endDate = doc['dataset']['coverage']['temporalCoverage'][0]['endDate'][0]
   if doc['dataset']['coverage']['temporalCoverage'][0].__class__.__name__ == 'list':
      endDate = doc['dataset']['coverage']['temporalCoverage'][0][0]
   pubDate = datetime.strptime(str(doc['dataset']['pubDate'])+"-01-01", date_format) 
   expTime = datetime.strptime(endDate.decode("utf8"), date_format) - datetime.strptime(beginDate.decode("utf8"), date_format)
   paperWriteTime = pubDate - datetime.strptime(endDate.decode("utf8"), date_format)
   #print "Experiment last: "+str(expTime.days)+" time between exp. and pub.: "+str(paperWriteTime.days)
   expTimes.append(expTime.days)
   pubTimes.append(paperWriteTime.days)   


import numpy as np
from matplotlib import pyplot
expArray = np.array(expTimes).astype(float)
pubArray = np.array(pubTimes).astype(float)

coefArray = np.divide(expArray,pubArray)

bins = np.linspace(-10, 10, 10)
n = len(expArray)
#pyplot.hist(expArray[1:n], bins, normed=1,histtype='stepfilled', alpha=0.5)
#pyplot.hist(pubTimes[1:n], bins, normed=1,histtype='stepfilled', alpha=0.5)
pyplot.hist(np.divide(expArray[1:n], pubArray[1:n]), bins, normed=1, histtype='stepfilled', alpha=0.5)
pyplot.gca().set_xlim([0, n])
pyplot.gca().set_ylim([min(min(expArray), min(pubArray)), max(max(expArray), max(pubArray))])
#pyplot.semilogy()
pyplot.show()

