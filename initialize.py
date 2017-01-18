from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from databases import Base, users, books

engine = create_engine('sqlite:///databases.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine



DBSession = sessionmaker(bind=engine)
session = DBSession()