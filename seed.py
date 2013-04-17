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

# 

# item = model.Item(name="Special Education Tutoring", description="Private tutoring sessions for your K-5 special needs child from a certified Special Education Teacher", user_id=3)
# session.add(item)

# user = model.User(email="jon@jonlattif.com", password="jonathan", first_name="Jonathan", last_name="Lattif", zipcode="07670", biz_name="Lattif Photography", website="www.lattifphotography.com")
# session.add(user)

# item = model.Item(name="Professional Photo Shoot", description="1, 2 or 3-hour photo shoot with a skilled professional photographer -- capture birthdays, family portraits, pet antics or other special occasions.", user_id=4)
# session.add(item)

item = model.Item(name="Green Services", description="Everyone's favorite tasty greens served up the way you want.", user_id=4)
session.add(item)


session.commit() # commit the change to the db

