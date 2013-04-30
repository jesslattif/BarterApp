
from flask import Flask, flash, render_template, redirect, request, session, url_for, g
import model
from model import User, Item, Participant, Trade, Category, session as db_session
import json

app  = Flask(__name__)
app.secret_key ="RZEB`YhM#EO|rhVWx~|U9,iYauiv l7B1t=ntDr7l-W&aM}JS2%"


#Before request - happens before every route
@app.before_request
def before_request():
	# Global variable scoped to request
	g.user_id = session.get("user_id") #gets user ID from current session
	if not g.user_id: # redirects to log-in if no user ID session
		g.user_id = None
		g.user = None
	else:
		g.user = db_session.query(User).get(g.user_id)
	


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
	error = None
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
	flash("Congrats! You're all set to start creating your profile.", "success")
	return redirect(url_for('home'))


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
		flash("Log-in failed; please try again.", "error")
		return render_template('index.html')


	else:
		print "SUCCEEDED" 
		session["user_id"] = user.id #set session
		flash("Login Successful", "success")
		return redirect(url_for('home')) #redirects to user's page for unique user id


"""Go to user's homepage"""

@app.route("/home")
def home():
	user = db_session.query(User).get(g.user_id)
	return render_template("home.html", user=user)

@app.route("/my_barter_profile")
def my_barter_profile():
	user = db_session.query(User).get(g.user_id)
	user_name = user.first_name

	return render_template(
		"my_barter_profile.html", user_name = user_name)

@app.route("/log_out", methods=['GET'])
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
#gets user object based on user_id
	user = db_session.query(User).get(g.user_id) 
	items = user.items 
	return render_template("manage_items.html", 
							user_items =items, user=user)


"""Delete Item"""

@app.route("/delete_item", methods=["POST"])
def delete_item():
	user = db_session.query(User).get(g.user_id)
	item = db_session.query(Item).get(request.args.get("id"))
	db_session.delete(item)
	db_session.commit()
	flash("item deleted", "info")
	return redirect(url_for('manage_items'))



"""Add new item"""
@app.route('/add_item')
def add_item():
	cats = db_session.query(Category).all()
	cats_json = json.dumps([cat.json() for cat in cats]) 	#turns list into json
	# Get all categories 
	# Put all categories into a list
	# Send list with template
		
	return render_template("add_item.html", 
							user=g.user_id, cats=cats_json)


@app.route("/insert_item", methods=["POST"])
def insert_item():
	user = db_session.query(User).get(g.user_id)#get user
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
	item = db_session.query(Item).get(id)
	return render_template("/edit_item.html", item=item)


"""Update edited item name"""

@app.route("/update_item", methods=["POST"])
def update_item():
	item = db_session.query(Item).get(request.args.get("id"))
	name_string = str(request.form["name"]) # takes in updated item name as string
	item.name = name_string
	db_session.commit()
	return redirect("/manage_items")

"""Change Item Description"""

@app.route("/edit_description/<int:id>", methods=["Get"])
def edit_description(id):
	item = db_session.query(Item).get(id)
	return render_template("/edit_description.html", item=item)

"""Update Item Description"""

@app.route("/update_description", methods=["POST"])
def update_description():
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
	# get all categories of type "goods"
	goods = db_session.query(Category).filter_by(cat_type=1).all()
	#get all categories of type "services"
	services = db_session.query(Category).filter_by(cat_type=2).all()
	return render_template("view_categories.html",
							goods=goods, services=services)

""" Search for Items in all Categories"""
@app.route("/search_all_cats", methods=["GET"])
def search_all_cats():
	# get search term from request args	
	search_term = request.args.get("search_term", '')
	if search_term == '':
		flash("Please enter a valid search term", "error")
		return redirect(url_for("view_categories"))
	# get items with name matching search term
	items = db_session.query(Item).filter(Item.name.like(
		"%" + search_term + "%")).filter(Item.user_id != g.user.id).all()
	if not items:
		flash("Sorry, nothing matched your search.", "error")
		return redirect(url_for("view_categories"))
	return render_template("display_items.html",
							items=items,
							search_term=search_term, title = "All items matching ")


"""View all items in a Category"""

@app.route("/display_items/<int:cat_id>", methods=["GET"])
def display_items(cat_id):
	#get all items for a category by cat_id
	items = db_session.query(Item).filter_by(cat_id=cat_id).filter(Item.user_id != g.user.id).all()
	cat = db_session.query(Category).filter_by(id=cat_id).one()
	# get category to display its name
	if not items:
		flash("Sorry, no items are available to trade in that category", "error")
		return redirect(url_for("view_categories"))
	return render_template(
		"display_items.html", items=items, search_term=cat.name, title="All items in ")

""" Click on an item to see users who've posted them """

@app.route("/display_user/<int:id>", methods=["GET"])
def display_user(id):
	#get all user who listed a particular item
	user = db_session.query(User).filter_by(id=id).one()
	#get all items for a particular user
	items = user.items
	return render_template("display_user.html", user=user, items=items)
	pass

"""See All Users & their items"""
@app.route("/user_list")
def user_list():
	pass


@app.route("/find_people")
def find_people():
	pass



######################################################
######################################################
######### These are the Trade functions #########
#####################################################
#####################################################

""" Open a trade request with another user """

@app.route("/open_request", methods=["GET", "POST"])
def open_request():
	#serve a form
	if request.method == "POST":
		flash("Trade Successfully Requested!", "success")
		return redirect(url_for('my_barter_profile'))
	# get item id from url
	item_id = request.args.get("item")
	# get entire item from DB
	item = db_session.query(Item).filter_by(id=item_id).one()
	return render_template("open_request.html", item=item)
	
	

	""" create a Participant B (not self) in the Trade with:
		# user_id 
		# item_id 
		# trade_id
		# total_qty ** need from form **
		# current_qty = 0
		# confirm = False

		create Participant A (self) in the Trade with:
		# user_id - g.user_id
		# item_id - ** need from form **
		# trade_id - 
		# total_qty ** need from form **
		# current_qty = 0
		# confirm  = False
		"""


@app.route("/manage_trades")
def manage_trades():
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
