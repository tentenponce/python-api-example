from connection import Base
from sqlalchemy import Column, String, Integer
from .baseModel import DictSerializable

class Stock(Base, DictSerializable):
	__tablename__ = "stock"
	
	id = Column(Integer, primary_key=True)
	name = Column(String)
	description = Column(String)
	
	def __init__(self, name, description):
		self.name = name
		self.description = description