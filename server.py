
from flask import Flask, render_template, redirect, request, session, url_for
import model
from model import User, Item, Participant, Trade, Category, session as db_session
import json

app  = Flask(__name__)
app.secret_key ="RZEB`YhM#EO|rhVWx~|U9,iYauiv l7B1t=ntDr7l-W&aM}JS2%"


"""Index""" 

@app.route("/")
def index():
	return render_template("index.html")



######################################################
######################################################
######### These are the user functions #########
######################################################
######################################################


	"""Sign up page"""

@app.route("/sign_up")
def sign_up():
	return render_template("sign_up.html")



"""Create a new user""" 

@app.route("/save_new_user", methods=["POST"])
def save_new_user(): 
	new_user = User(email=request.form["email"], 
					password=request.form["password"], 
					first_name=request.form["first_name"], 
					last_name=request.form['last_name'], 
					biz_name=request.form['biz_name'], 
					website=request.form['website'], 
					zipcode=request.form["zipcode"])
	db_session.add(new_user) #add & commit new user
	db_session.commit()
	session["user_id"] = user.id
	return redirect(url_for('my_barter_profile'))


"""Log-in"""

@app.route("/log_in")
def log_in():
	return render_template("log_in.html")


"""Authenticate User"""

@app.route("/authenticate", methods=["POST"])
def authenticate(): # authenticate user
	email = request.form['email']
	password = request.form['password']
	user = db_session.query(User).filter_by(
		email=email, password=password).first() #checks for user in db

	if not user: #redirect to log-in if info not correct
		print "FAILED LOGIN"
		return redirect(url_for('index'))


	print "SUCCEEDED" 
	session["user_id"] = user.id #set session
	return redirect(url_for('home')) #redirects to user's page for unique user id


"""Go to user's homepage"""

@app.route("/home")
def home():
	user_id = session.get("user_id") #gets user ID from current session
	if not user_id: # redirects to log-in if no user ID session
		return redirect(url_for("index"))

	user = db_session.query(User).get(user_id)
	user_name = user.first_name

	return render_template("home.html", user_name=user_name)

@app.route("/my_barter_profile")
def my_barter_profile():
	user_id = session.get("user_id") #gets user ID from current session
	if not user_id: # redirects to log-in if no user ID session
		return redirect(url_for("index"))
	user = db_session.query(User).get(user_id)
	user_name = user.first_name

	return render_template(
		"my_barter_profile.html", user_name = user_name)

@app.route("/log_out", methods=['POST'])
def log_out():
	session.pop("user_id", None)
	return redirect("/")

######################################################
######################################################
######### These are the Item functions #########
#####################################################
#####################################################


"""See all of User's Items """

@app.route("/manage_items")
def manage_items():
	user_id = session.get("user_id")
	if not user_id: # redirects to log-in if no user ID session
		redirect(url_for("index"))

	user = db_session.query(User).get(user_id) #gets user object based on user_id
	items = user.items 
	return render_template("manage_items.html", 
							user_items =items, user=user)


"""Delete Item"""

@app.route("/delete_item", methods=["POST"])
def delete_item():
	user_id = session.get("user_id")
	if not user_id: # redirects to log-in if no user ID session
		return redirect(url_for("index"))
	user = db_session.query(User).get(user_id)
	item = db_session.query(Item).get(request.args.get("id"))
	db_session.delete(item)
	db_session.commit()
	return render_template("/item_deleted.html")



"""Add new item"""
@app.route('/add_item')
def add_item():
	user_id = session.get("user_id")
	if not user_id: # redirects to log-in if no user ID session
		return redirect(url_for("index"))
	cats = db_session.query(Category).all()
	cats_json = json.dumps([cat.json() for cat in cats]) 	#turns list into json
	# Get all categories 
	# Put all categories into a list
	# Send list with template
		
	return render_template("add_item.html", 
							user=user_id, cats=cats_json)


@app.route("/insert_item", methods=["POST"])
def insert_item():
	user_id = session.get("user_id")
	if not user_id: # redirect to log-in if no user ID session
		return redirect(url_for("index"))
	user = db_session.query(User).get(user_id)#get user
	name_string = str(request.form["name"]) #take in new item name as a string
	descr_string = str(request.form["description"]) #take in new item description as a string 
	cat_id= int(request.form["category"]) #take in cat id as integer
	new_name = Item(
		name=name_string, description=descr_string,
		cat_id=cat_id) #creates new item object from user's input
	new_name.user = user #attach item object to user object
	
	db_session.commit()
	return redirect(url_for('manage_items'))


"""Edit item name"""

@app.route("/edit_item/<int:id>", methods=["GET"])
def edit_item(id):
	user_id = session.get("user_id")
	if not user_id: # redirects to log-in if no user ID session
		return redirect(url_for("index"))
	item = db_session.query(Item).get(id)
	return render_template("/edit_item.html", item=item)


"""Update edited item name"""

@app.route("/update_item", methods=["POST"])
def update_item():
	user_id = session.get("user_id")
	if not user_id: # redirects to log-in if no user ID session
		return redirect(url_for("index"))
	user = db_session.query(User).get(user_id)
	item = db_session.query(Item).get(request.args.get("id"))
	name_string = str(request.form["name"]) # takes in updated item name as string
	item.name = name_string
	db_session.commit()
	return redirect("/manage_items")

"""Change Item Description"""

@app.route("/edit_description/<int:id>", methods=["Get"])
def edit_description(id):
	user_id = session.get("user_id")
	if not user_id: # redirects to log-in if no user ID session
		return redirect(url_for("index"))
	item = db_session.query(Item).get(id)
	return render_template("/edit_description.html", item=item)

"""Update Item Description"""

@app.route("/update_description", methods=["POST"])
def update_description():
	user_id = session.get("user_id")
	if not user_id: # redirects to log-in if no user ID session
		return redirect(url_for("index"))
	user = db_session.query(User).get(user_id) #gets user id
	item = db_session.query(Item).get(request.args.get("id")) #gets item id
	descr_string = str(request.form["description"]) #takes in new description as string
	item.description = descr_string
	db_session.commit()
	return redirect("/manage_items")


######################################################
######################################################
######### These are the Search functions #########
#####################################################
#####################################################

"""View All Categories"""

@app.route("/view_categories", methods=["GET"])
def view_categories():
	user_id = session.get("user_id")
	if not user_id: # redirects to log-in if no user ID session
		return redirect(url_for("index"))
	# get all categories of type "goods"
	goods = db_session.query(Category).filter_by(cat_type=1).all()
	#get all categories of type "services"
	services = db_session.query(Category).filter_by(cat_type=2).all()
	return render_template("view_categories.html",
							goods=goods, services=services)


"""View all items in a Category"""

@app.route("/display_items/<int:cat_id>", methods=["GET"])
def display_items(cat_id):
	user_id = session.get("user_id")
	if not user_id: # redirects to log-in if no user ID session
		return redirect(url_for("index"))
	#get all items for a category by cat_id
	items = db_session.query(Item).filter_by(cat_id=cat_id).all()
	cat = db_session.query(Category).filter_by(id=cat_id).one()
	return render_template("display_items.html", items=items, cat=cat)
	pass

""" Click on an item to see users who've posted them """

@app.route("/display_users/", methods=["GET"])
def display_users(item_id):
	user_id = session.get("user_id")
	if not user_id: # redirects to log-in if no user ID session
		return redirect(url_for("index"))
	#get all users who have listed a particular item
	users = db_session.query(User).filter_by(item_id=item_id).all()
	return render_template("display_users.html", users=users)
	pass

"""See All Users & their items"""
@app.route("/user_list")
def user_list():
	user_id = session.get("user_id")
	if not user_id: # redirects to log-in if no user ID session
		return redirect(url_for("index"))
	pass


@app.route("/find_people")
def find_people():
	user_id = session.get("user_id")
	if not user_id: # redirects to log-in if no user ID session
		return redirect(url_for("index"))
	pass


@app.route("/open_request")
def open_request():
	user_id = session.get("user_id")
	if not user_id: # redirects to log-in if no user ID session
		return redirect(url_for("index"))
	pass


######################################################
######################################################
######### These are the Trade functions #########
#####################################################
#####################################################



@app.route("/manage_trades")
def manage_trades():
	user_id = session.get("user_id")
	if not user_id: # redirects to log-in if no user ID session
		return redirect(url_for("index"))
	pass

######################################################
######################################################
######### These are the Trade functions #########
#####################################################
#####################################################

@app.route("/manage_account")
def manage_account():
	pass



if __name__ == "__main__":
	app.run(debug = True)
