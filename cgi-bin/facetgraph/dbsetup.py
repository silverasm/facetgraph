import sys
import os
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapper

# set up the database session
engine = create_engine("mysql://dig:dig@bigdb.xcloud.fxpal.net/dig")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base(bind=engine)
Base.metadata.create_all(engine) 

"""
	The data structures
"""
class RI(Base):
	"""
		A general reverted index class
	"""
	__tablename__ = "RI"
	id = Column(Integer, primary_key=True)
	query = Column(String(50))
	queryType = Column(String(20))
	result = Column(String(50))
	resultType = Column(String(20))
	rank = Column(Integer)
	score = Column(Float)
	
	def __init__(self, query, queryType, result, resultType, rank, score):
		self.query = query
		self.queryType = queryType
		self.result = result
		self.resultType = resultType
		self.rank = rank
		self.score = score
	
	def __repr__(self):
		return "<%s - %s: %.2f (%d)>"%(self.query, self.result, self.score, self.rank)

"""
	Features of a camera
"""

class ShortFeature(Base):
	__tablename__ = "shortfeature"
	id = Column(Integer, primary_key=True)
	shortFeature = Column(String(50))
	longFeatureID = Column(Integer)
	
	def __init__(self, shortFeature, longFeatureID):
		self.shortFeature = shortFeature
		self.longFeatureID = longFeatureID
	
	def __repr__(self):
		return "<ShortFeature %s (%d)>"%(self.shortFeature, self.longFeatureID)

shortFeatureIndex = {}
for feature in session.query(ShortFeature):
	shortFeatureIndex[feature.shortFeature] = feature.longFeatureID

class Feature(Base):
	__tablename__ = "feature"
	id = Column(Integer, primary_key=True)
	feature = Column(String(500))
	pmi = Column(Float)
	
	def __init__(self, feature, pmi):
		self.feature = feature
		self.pmi = pmi
	
	def __repr__(self):
		return "<Feature %s (%.2f)>"%(self.feature, self.pmi)
featureIndex = {}
for feature in session.query(Feature):
	featureIndex[feature.feature] = feature.id

	
def getFeatureID(featureName):
	if featureName in featureIndex:
		return featureIndex[featureName]
	else:
		return shortFeatureIndex[featureName]

def getFeatureName(id):
	instance = session.query(Feature).filter(Feature.id == id)[0]
	return instance.feature.split(",")[0]
"""
	Cameras
"""
cameras = Table('camera', Base.metadata, autoload=True)
class Camera(object):
	def __init__(self, asin, make, model, imageUrl, price, priceFormatted, totalReviews, averageRating, fromFlickr, barcodeSmall, barcodeLarge):
		 self.asin = asin
		 self.make = make
		 self.model = model
		 self.imageUrl = imageUrl
		 self.price = price
		 self.priceFormatted = priceFormatted
		 self.totalReviews = totalReviews
		 self.averageRating = averageRating
		 self.fromFlickr = fromFlickr
		 self.barcodeSmall = barcodeSmall
		 self.barcodeLarge = barcodeLarge
	
	def __repr__(self):
		return "<Camera %s %s>"%(self.make, self.model)

mapper(Camera, cameras)
index = {}
for camera in session.query(Camera):
	index["%s %s"%(camera.make, camera.model)] = camera.id
	
def getCameraID(cameraName):
	return index[cameraName]

def getCameraName(id):
	instance = session.query(Camera).filter(Camera.id==id)[0]
	return instance.make +" "+instance.model
"""
	Feature-to-Camera Index
"""
class fcRevertedIndex(Base):
	__tablename__ = 'featureCameraRI'
	
	id = Column(Integer, primary_key=True)
	query = Column(Integer)
	result = Column(Integer)
	score = Column(Float)
	rank = Column(Integer)
	fn = Column(String(200))
	
	def __init__(self, query, result, rank, score, fn):
		self.query = query
		self.result = result
		self.rank = rank
		self.score = score
		self.fn = fn
	
	def __repr__(self):
		return "<fcRevertedIndex(%d, %d, %d, %.2f - %s)>"%(self.query, self.result, self.rank, self.score, self.fn)

"""
	Camera-To-Feature Index
"""
class cfRevertedIndex(Base):
	__tablename__ = 'cameraFeatureRI'
	
	id = Column(Integer, primary_key=True)
	query = Column(Integer)
	result = Column(Integer)
	score = Column(Float)
	rank = Column(Integer)
	fn = Column(String(200))
	
	def __init__(self, query, result, rank, score, fn):
		self.query = query
		self.result = result
		self.rank = rank
		self.score = score
		self.fn = fn
	
	def __repr__(self):
		return "<fcRevertedIndex(%d, %d, %d, %.2f - %s)>"%(self.query, self.result, self.rank, self.score, self.fn)
	