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
# item = model.Item(
# 				user_id=1,
# 				name="Fish", 
# 				description="fresh, local, sustainable seafood brought to you by Fair Share CSF", 
# 				owned=True)
# session.add(item)


# item = model.Item(
# 				user_id=2, 
# 				name="Policy Analysis",
# 				description="Sharp, thoughtful policy analysis by an exciting and accomplished analyst",
# 				owned=True)
# session.add(item)


# 3,Fashion advice,"The most cutting-edge, fashion-forward style tips from renowned fashion writer Rachelle B.",3
# 4,Tutoring,Home or library-based tutoring for your k-5 students by an accredited special education tutor,4
# 5,Photography,1 hour photo shoot including two prints of your choice,5

# item = model.Item(name="Special Education Tutoring", description="Private tutoring sessions for your K-5 special needs child from a certified Special Education Teacher", user_id=3)
# session.add(item)

# user = model.User(email="jon@jonlattif.com", password="jonathan", first_name="Jonathan", last_name="Lattif", zipcode="07670", biz_name="Lattif Photography", website="www.lattifphotography.com")
# session.add(user)

# item = model.Item(name="Professional Photo Shoot", description="1, 2 or 3-hour photo shoot with a skilled professional photographer -- capture birthdays, family portraits, pet antics or other special occasions.", user_id=4)
# session.add(item)

category = model.Category(
	cat_type=1, name="Art, Antiques & Collectibles")
session.add(category)

category = model.Category(
	cat_type=2, name="Accounting, Finance & Legal")
session.add(category)

category = model.Category(
	cat_type=2, name="Food & Nutrition")
session.add(category)

category = model.Category(
	cat_type=1, name="Media & Entertainment")
session.add(category)

category = model.Category(
	cat_type=2, name="Health, Fitness & Beauty")
session.add(category)

category = model.Category(
	cat_type=2, name="Software & Web Development")
session.add(category)

category = model.Category(
	cat_type=1, name="Electronics & Devices")
session.add(category)

category = model.Category(
	cat_type=2, name="Medical & Dental")
session.add(category)

category = model.Category(
	cat_type=2, name="Vehicle Maintenance & Repair")

category = model.Category(
	cat_type=1, name="Vehicle Parts")
session.add(category)

category = model.Category(
	cat_type=1, name="Clothing, Jewelry & Accessories")
session.add(category)

category = model.Category(
	cat_type=1, name="Food & Beverage")
session.add(category)

session.commit() # commit the change to the db

