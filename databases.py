
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from flask import *
from passlib.apps import custom_app_context as pwd_context
Base = declarative_base()


class Book(Base):
	__tablename__ = 'Books'
	id = Column(Integer, primary_key=True)
	title = Column(String)
	author = Column(String)
	pubyear = Column(String)
	imgurlbook = Column(String)
	genre = Column(String)
	location = Column(String)

class User(Base):
	__tablename__ = 'Users'
	id = Column(Integer, primary_key=True)
	firstname = Column(String)
	lastname = Column(String)
	email = Column(String, unique=True)
	password = Column(String)
	hash_password=Column(String(255))
	imgurluser = Column(String)
	dob = Column(String)
	phonenumber = Column(String)


	def hash_password(self, password):
		self.hash_password = pwd_context.encrypt(password)

	def verify_password(self, spassword):
		return pwd_context.verify(password, self.hash_password)







engine = create_engine('sqlite:///databases.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()
