from flask import *
from databases import *

session.add(users(firstname="nada"))
session.commit()
