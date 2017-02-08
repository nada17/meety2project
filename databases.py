
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from flask import *

Base = declarative_base()


class books(Base):
	__tablename__ = 'books'
	id = Column(Integer, primary_key=True)
	title = Column(String)
	author = Column(String)
	pubyear = Column(Date)
	imgurlbook = Column(String)
	genre = Column(String)
	location = Column(String)

class users(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	firstname = Column(String)
	lastname = Column(String)
	email = Column(String, unique=True)
	password = Column(String)
	imgurluser = Column(String)
	dob = Column(Date)
	phonenumber = Column(String)

	def hash_password(self, password):
		self.password_hash = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password_hash)




engine = create_engine('sqlite:///databases.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()
