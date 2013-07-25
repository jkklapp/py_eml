# Main python script to connect to DB, load some primitives to start working.
# You are supposed to have the EML documents in a local MongoDB instance and on
# a collection named 'all'.

from pymongo import MongoClient
from bson.code import Code
from bson.objectid import ObjectId
import logging
import matplotlib.pyplot as plt
import numpy as np
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

db = MongoClient('localhost',27777)
col = db.eml_docs.all

execfile('code/eml/py_eml/eml_mr.py')






