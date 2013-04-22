# Using PostgreSQL which I don't know, so not sure how to format these. 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, types 
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import sessionmaker, scoped_session 	#Describes how to interact with database, needs to be instantiated.
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import json

engine = create_engine("sqlite:///barters.db", echo=False) 		#Creates engine that connects to db.
session = scoped_session(sessionmaker(
									bind=engine, 
									autocommit = False, 
									autoflush = False)) #Sets a variable that will be used by sessionmaker to help interact with ratings.db; no need for the "connect()" function.

# the variable connecting to the declarative_base function of sqlalchemy - just do it!
Base = declarative_base()
Base.query = session.query_property()

def make_all():
	Base.metadata.create_all(engine)

#All users who sign up
class User(Base): 
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	email = Column(String)
	password = Column(String)
	first_name = Column(String)
	last_name = Column(String)
	zipcode = Column(String)
	biz_name = Column(String)
	website = Column(String)
	image_url = Column(String, nullable=True)
	opt_a = Column(String, nullable=True)
	opt_b = Column(String, nullable=True)
	opt_c = Column(String, nullable=True)


#All items users list for trading
class Item(Base): 
	__tablename__ = 'items'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	description = Column(String)
	owned = Column(Boolean)
	image_url = Column(String, nullable=True)
	user_id = Column(Integer, ForeignKey("users.id"))
	cat_id = Column(Integer, ForeignKey("categories.id"))
	user = relationship("User", backref=backref("items", order_by=id)) 
	category = relationship("Category", backref=backref("items", order_by=id))
	

#Transactions between participants(users)
class Trade(Base): 
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
	total_qty = Column(Integer) 
	current_qty = Column(Integer, nullable=True)
	confirm = Column(Boolean)
	user = relationship("User", backref=backref("participants"))
	item = relationship("Item", backref=backref("participants"))
	trade = relationship("Trade", backref=backref("participants"))


class Category(Base):
	__tablename__ = 'categories'

	id = Column(Integer, primary_key=True)
	name = Column(String)				#category of item listed
	cat_type = Column(Integer) 			#goods or services
	
	def json(self):
		return dict(
			name=self.name,
			cat_type=self.cat_type,
			id=self.id
			)


class Reviews(Base):
	__tablename__ = 'reviews'

	id = Column(Integer, primary_key=True)
	review = Column(String)
	rating = Column(Integer)
	trade_id = Column(Integer, ForeignKey("trades.id"))
	trade = relationship("Trade", backref=backref("reviews"))














