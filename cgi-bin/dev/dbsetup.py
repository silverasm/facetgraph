import sys
import os
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapper

# set up the database session
#engine = create_engine("mysql://dev:dev@localhost/development")
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


class WordAndCameraRI(Base):
	__tablename__ = "WordAndCameraRI"
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


class WordToWordRI(Base):
	__tablename__ = "wtowri"
	id = Column(Integer, primary_key=True)
	query = Column(String(50))
	result = Column(String(50))
	rank = Column(Integer)
	score = Column(Float)
	count = Column(Float)
	
	def __init__(self, query, result, rank, score, count):
		self.query = query
		self.result = result
		self.rank = rank
		self.score = score
		self.count = count
	
	def __repr__(self):
		return "<%s - %s: %.2f (%d)>"%(self.query, self.result, self.score, self.rank)

Base.metadata.create_all(engine)