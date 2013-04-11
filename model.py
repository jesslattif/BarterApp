# class Rating(Base):
# 	__tablename__ = "ratings"

# 	id = Column(Integer, primary_key=True)
# 	user_id = Column(Integer, ForeignKey("users.id"))
# 	movie_id = Column(Integer, ForeignKey("movies.id"))
# 	rating = Column(Integer)
# 	user = relationship("User", backref=backref("ratings", order_by=id))
# 	movie = relationship("Movie", backref=backref("ratings", order_by=id))

# ### "repr" function decodes ratings info in memory space into readable text
# 	def __repr__(self):
# 		return u"<Rating: %d %d %d %d>"%(self.id, self.user_id, self.movie_id, self.rating)



# 	# sqlalchemy writes the init function - if we write it then it overwrites and gets odd results
# 	# use named parameters email = ... 

class User(Base):
	id = Column(Integer, primary=True)
	email = Column(String(64))
	password = Column(String(64))
	username = Column(String(64))
	biz_name = Column(String(64))
	website = Column(String(255))
	opt_a = Column(String(255), nullable=True)
	opt_b = Column(String(255), nullable=True)
	opt_c = Column(String(255), nullable=True)


class Item(Base):
	id = Column(Integer, primary=True)
	name = Column(String(64))
	description = Column(String(512))
	user_id = Column(Integer, ForeignKey("users.id"))
	cat_id = Column(Integer, ForeignKey("categories.id"))
	user = relationship("User", backref=backref("users", order_by=id))
	category = relationship("Category", backref=backref("categories", order_by=id))

class Trade(Base):
	id = Column(Integer, primary=True)
	open_date = Column()
















