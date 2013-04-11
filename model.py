# USing PostgreSQL which I don't know, so not sure how to format these. 

class User(Base): #all users who sign up
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	email = Column(String(64))
	password = Column(String(64))
	username = Column(String(64))
	biz_name = Column(String(64))
	website = Column(String(255))
	image_url = Column(String(255))
	opt_a = Column(String(255), nullable=True)
	opt_b = Column(String(255), nullable=True)
	opt_c = Column(String(255), nullable=True)


class Item(Base): #specific items users list for trading
	__tablename__ = 'items'

	id = Column(Integer, primary_key=True)
	name = Column(String(64))
	description = Column(String(512))
	image_url = Column(String(255))
	user_id = Column(Integer, ForeignKey("users.id"))
	cat_id = Column(Integer, ForeignKey("categories.id"))
	user = relationship("User", backref=backref("users", order_by=id))
	category = relationship("Category", backref=backref("categories", order_by=id))

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
	trade_item_id = Column(Integer, ForeignKey("trades.id"))
	total_qty = Column(Integer) #should use "smallint"?
	current_qty = Column(Integer, nullable=True)
	confirm = Column(Boolean)#is this the right way to do this?

class Category(Base):
	__tablename__ = 'categories'

	id = Column(Integer, primary_key=True)
	good = Column(Boolean) #not sure how to do this -- if it's a good, it's not a service, and vice-versa
	service = Column(Boolean)
	name = Column(String(64))

class Reviews(Base):
	__tablename__ = 'reviews'
	id = Column(Integer, primary_key=True)
	review = Column(String(1024))
	rating = Column(Integer)
	trade_id = COlumn(Integer, ForeignKey("trades.id"))


















