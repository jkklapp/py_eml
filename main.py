'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
    Author: Jaakko Lappalainen, 2013. email: jkk.lapp@gmail.com
'''
'''
 Main python script to connect to DB, load some primitives to start working.
 You are supposed to have the EML documents in a local MongoDB instance and on
 a collection named 'all'.
'''
from pymongo import MongoClient
from bson.code import Code
from bson.objectid import ObjectId
import logging
import matplotlib.pyplot as plt
import numpy as np
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

db = MongoClient('localhost',27017)
col = db.eml_docs.all

execfile('code/eml/py_eml/eml_mr.py')






