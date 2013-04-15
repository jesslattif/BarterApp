# USing PostgreSQL which I don't know, so not sure how to format these. 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, types 
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import sessionmaker, scoped_session #like sqlite3 cursor - describes how to interact with database, needs to be instantiated
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

engine = create_engine("sqlite:///barters.db", echo=False) #creates engine that connects to db
session = scoped_session(sessionmaker(bind=engine, autocommit = False, autoflush = False)) # set a variable that will be used by sessionmaker to help interact with ratings.db, now we don't need the "connect()" function

# the variable connecting to the declarative_base function of sqlalchemy - just do it!
Base = declarative_base()
Base.query = session.query_property()

def make_all():
	Base.metadata.create_all(engine)

class User(Base): #all users who sign up
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	email = Column(String(64))
	password = Column(String(64))
	first_name = Column(String(64))
	last_name = Column(String(64))
	zipcode = Column(String(16))
	biz_name = Column(String(64))
	website = Column(String(255))
	image_url = Column(String(255), nullable=True)
	opt_a = Column(String(255), nullable=True)
	opt_b = Column(String(255), nullable=True)
	opt_c = Column(String(255), nullable=True)



class Item(Base): #specific items users list for trading
	__tablename__ = 'items'

	id = Column(Integer, primary_key=True)
	name = Column(String(64))
	description = Column(String(512))
	image_url = Column(String(255), nullable=True)
	user_id = Column(Integer, ForeignKey("users.id"))
	cat_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
	user = relationship("User", backref=backref("items", order_by=id)) 
	category = relationship("Category", backref=backref("items", order_by=id))

class Trade(Base): #transactions between participants(users)
	__tablename__ = 'trades'

	id = Column(Integer, primary_key=True)
	open_date = Column(Date) #timestamp?
	transaction_date = Column(Date)
	close_date = Column(Date)

class Participant(Base): #participants in specific trades
	__tablename__ = 'participants'

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey("users.id"))
	item_id = Column(Integer, ForeignKey("items.id"))
	trade_id = Column(Integer, ForeignKey("trades.id"))
	total_qty = Column(Integer) #should use "smallint"?
	current_qty = Column(Integer, nullable=True)
	confirm = Column(Boolean)#Integer is a placeholder for Boolean cuz don't know how to set this up
	user = relationship("User", backref=backref("participants"))
	item = relationship("Item", backref=backref("participants"))
	trade = relationship("Trade", backref=backref("participants"))


class Category(Base):
	__tablename__ = 'categories'

	id = Column(Integer, primary_key=True)
	cat_type = Column(Integer, ForeignKey("types.id")) #not sure how to do this -- if it's a good, it's not a service, and vice-versa, Integer is a placeholder for Boolean cuz don't know how to set this up
	name = Column(String(64))
	category = relationship("Cat_type", backref=backref("categories"))

class Reviews(Base):
	__tablename__ = 'reviews'
	id = Column(Integer, primary_key=True)
	review = Column(String(1024))
	rating = Column(Integer)
	trade_id = Column(Integer, ForeignKey("trades.id"))
	trade = relationship("Trade", backref=backref("reviews"))


class Cat_type(Base):
	__tablename__ = 'types'

	id = Column(Integer, primary_key=True)
	name = Column(String(64)) #0 = good 1 = service



















