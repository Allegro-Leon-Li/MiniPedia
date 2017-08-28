import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, Category, CategoryItem


engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
cat1 = Category(name = "Soccer")
cat2 = Category(name = "Basketball")
it1 = CategoryItem(name = "Buffon Jersey", description = "Gigi Buffon signed", category = cat1)
it1_1 = CategoryItem(name = "Soccer ball", description = "a ball", category = cat1)
it2 = CategoryItem(name = "Basketball Shoes", description = "a shoe", category = cat2)
session.add(cat1)
session.add(cat2)
session.add(it1)
session.add(it1_1)
session.add(it2)
session.commit()