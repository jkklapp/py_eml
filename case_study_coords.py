'''
    Author: Jaakko Lappalainen, 2013. email: jkk.lapp@gmail.com
'''
'''
 This code implements the case study on spatial coverage 
'''



''' More comfortable data stricture '''

sites = ['and','bes','bnz','cdr','cwt','fce','gce','jrn','mcm','pie','vcr']

data = {}
for site in sites:
	col = db[site]
	for doc in col.find():
		try:
			data[doc['_id']] = doc['dataset']['coverage'][u'geographicCoverage'][u'boundingCoordinates']
		except TypeError:
			pass
		except KeyError:
			print doc['dataset'].keys()
			pass


data2 = {}
for site in sites:
	col = db[site]
	for doc in col.find():
		try:
			data2[doc['_id']] = doc['dataset']['coverage'][0][u'boundingCoordinates']
		except TypeError:
			pass
		except KeyError:
			print doc['dataset'].keys()
			pass

'''Check how many docs are not in data or data2'''

for site in sites:
	col = db[site]
	for doc in col.find():
		if doc['_id'] not in data.keys() and doc['_id'] not in data2.keys():
			try:
				print doc['dataset']['coverage']
			except KeyError:
				pass


''' Now let's get an array for numpy '''
import unicodedata
l = []
for key in data.keys():
	coords = data[key]
	try:
		l.append([float(str(coords['westBoundingCoordinate'])), float(str(coords['northBoundingCoordinate']))])
		l.append([float(str(coords['eastBoundingCoordinate'])), float(str(coords['northBoundingCoordinate']))])
		l.append([float(str(coords['westBoundingCoordinate'])), float(str(coords['southBoundingCoordinate']))])
		l.append([float(str(coords['eastBoundingCoordinate'])), float(str(coords['southBoundingCoordinate']))])
	except ValueError:
		pass

for key in data2.keys():
	coords = data2[key]
	try:
		l.append([float(str(coords['westBoundingCoordinate'])), float(str(coords['northBoundingCoordinate']))])
		l.append([float(str(coords['eastBoundingCoordinate'])), float(str(coords['northBoundingCoordinate']))])
		l.append([float(str(coords['westBoundingCoordinate'])), float(str(coords['southBoundingCoordinate']))])
		l.append([float(str(coords['eastBoundingCoordinate'])), float(str(coords['southBoundingCoordinate']))])
	except ValueError:
		pass



import numpy
import matplotlib
matplotlib.use('Agg')
from scipy.cluster.vq import *
import pylab
pylab.close()


numData = numpy.array(l)


from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def draw_screen_poly( lats, lons, m, color):
    x, y = m( lons, lats )
    xy = zip(x,y)
    poly = Polygon( xy, facecolor=color, alpha=0.4 )
    plt.gca().add_patch(poly)

lats = [ -30, 30, 30, -30 ]
lons = [ -50, -50, 50, 50 ]

m = Basemap(projection='sinu',lon_0=0)
m.drawcoastlines()
m.drawmapboundary()
draw_screen_poly( lats, lons, m, 'red')

plt.show()


'''
'''

plt.plot(*zip(*a))
# generate some random xy points and
# give them some striation so there will be "real" groups.
'''
xy = numpy.random.rand(30,2)
xy[3:8,1] -= .9
xy[22:28,1] += .9
'''
xy = numData

# make some z vlues
z = numpy.sin(xy[:,1]-0.2*xy[:,1])

# whiten them
z = whiten(z)

# let scipy do its magic (k==3 groups)
#res, idx = kmeans2(numpy.array(zip(xy[:,0],xy[:,1],z)),3)
res, idx = kmeans2(numpy.array(zip(xy[:,0],xy[:,1],z),3))

# convert groups to rbg 3-tuples.
colors = ([([0,0,0],[1,0,0],[0,0,1])[i] for i in idx])

# show sizes and colors. each color belongs in diff cluster.
pylab.scatter(xy[:,0],xy[:,1],s=20*z+9, c=colors)
pylab.savefig('/var/www/tmp/clust.png')