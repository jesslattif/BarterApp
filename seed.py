import model
from model import session
model.make_all()

# id = Column(Integer, primary_key=True)
# 	email = Column(String(64))
# 	password = Column(String(64))
# 	first_name = Column(String(64))
# 	last_name = Column(String(64))
# 	zipcode = Column(String(16))
# 	biz_name = Column(String(64))
# 	website = Column(String(255))

# user = model.User(email='jesslattif@gmail.com', password='jessica',first_name='Jessica',last_name="Lattif",zipcode ="94538",biz_name="Fair Share CSF", website="www.fairsharecsf.com")
# session.add(user) # add the user to sesion to pass it to the db

# user = model.User(email="jalal.elhayek@gmail.com", password="jalal", first_name="Jalal", last_name="Elhayek", zipcode="94538", biz_name="Fair Share CSF", website="www.fairsharecsf.com")
# session.add(user)

item = model.Item(name="fish", description="sustainable local seafood from Fair Share CSF", user_id=1)
session.add(item)

item = model.Item(name="shellfish", description="sustainably-farmed shellfish from Tomales Bay, brought to you by Fair Share CSF", user_id=2)
session.add(item)


session.commit() # commit the change to the db

