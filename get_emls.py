import urllib2
import xmltodict
import xml.etree.ElementTree as ET
from pymongo import MongoClient
import json
import pymongo
import sys
import uuid
import os

sources=[

'http://lterweb.forestry.oregonstate.edu/lterhja/harvestList.pl',
'http://ecosystems.mbl.edu/ARC/eml_harvest/harvestlist.xml',
'http://beslter.org/metacat_harvest/harvestlist.xml',
'http://www.lter.uaf.edu/eml/BNZHarvestList.xml',
'http://caplter.asu.edu/home/data/HarvestList.jsp',
'http://www.cedarcreek.umn.edu/data/CDRharvestList.xml',
'http://coweeta.ecology.uga.edu/harvestlist/harvestList.xml',
'http://fcelter.fiu.edu/data/metadata/EML/FCEHarvestList.xml',
'http://gce-lter.marsci.uga.edu/lter/asp/db/eml_harvest_doc.asp',
'http://www.hubbardbrook.org/eml/hb_harvest_list.xml',
'http://harvardforest.fas.harvard.edu/data/eml/harvestList.xml',
'http://jornada-www.nmsu.edu/ims/site/harvest/eml/jrn_metacat_harvest_list.xml',
'http://lter.kbs.msu.edu/Data/LTER_Metadata.jsp?Dataset=all&stylesheet=Metacat.xsl',
'http://www.konza.ksu.edu/konza/misc/metacat_knzlist.xml',
'http://luq.lternet.edu/EcologicalMetadataLanguage/LUQEMLFiles/LUQHarvestList.xml',
'http://cvs.lternet.edu/cgi-bin/viewcvs.cgi/*checkout*/NIS/projects/remoteSensing/harvestList.xml?rev=HEAD&only_with_tag=MAIN&content-type=text/xml',
'http://www.mcmlter.org/data/eml_harvest/MCMharvestList.xml',
'http://mcr.lternet.edu/metadata/harvestlist.xml',
'http://culter.colorado.edu/Harvest/NWTHarvestList.xml',
'http://lterquery.limnology.wisc.edu/eml/harvest/',
'http://ecosystems.mbl.edu/pie/data/eml/PIEharvestList.xml',
'http://sev.lternet.edu/data/sevharvestlist.xml',
'http://sgs.cnr.colostate.edu/Data/EML/SGSHarvestList.xml',
'http://www.vcrlter.virginia.edu/data/query/text/eml/eml_list.xml'


]

client = MongoClient('localhost', 4000)
db = client.eml_docs
url = sys.argv[1]

try:
	response = urllib2.urlopen(url)
except:
	print "URL not available: "+url
	sys.exit(-1)
content = response.read()
	#content = open(filename,'r').read().replace('\r\n','')
try:
	root = ET.fromstring(content)
except:
	print "Error parsing XML... "+url
	print ""
	print content
	print ""
	sys.exit(-1)

siteName=root[0][0][0].text.replace('knb-lter-','')

if len(sys.argv) == 2:
	col = db[siteName]
else:
	col = db[sys.argv[2]]

for e in root.findall(".//documentURL"):
	try:
		responseEML = urllib2.urlopen(e.text)
	except:
		print siteName+": Error retrieving EML document..."
		continue
	emldoc_content = responseEML.read()
	try:
		o = xmltodict.parse(emldoc_content)
	except:
		print ""
		print emldoc_content
		print ""
		print siteName+": Error parsing EML document..."
		continue
	try:
		s = col.insert(o)
	except pymongo.errors.DuplicateKeyError:
		print siteName+": (Mongo) duplicateKeyError!!!"
		continue

