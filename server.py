
from flask import Flask, flash, render_template, redirect, request, session, url_for, g
import model
from model import User, Item, Participant, Trade, Category, session as db_session
import json
import datetime

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
		g.notifications, g.new_confirms = get_notifications()
		print "***************", g.notifications



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
		flash("Sorry, we couldn't find your email/password combo. Try again!", "error")
		return render_template('index.html')


	else:
		
		session["user_id"] = user.id #set session
		flash("Login Successful", "success")
		return redirect(url_for('home')) #redirects to user's page for unique user id


"""Go to user's homepage"""

@app.route("/home")
def home():
	user = db_session.query(User).get(g.user_id)
	return render_template("home.html", user=user)

""" Log out """

@app.route("/log_out", methods=['GET'])
def log_out():
	session.pop("user_id", None)
	return redirect("/")


""" Edit User's Account Settings """

@app.route("/my_account")
def my_account():
	pass

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

""" Find businesses  """
@app.route("/find_business", methods=["GET"])
def find_business():
	search_term = request.args.get("search_term", '')
	if search_term == '':
		flash("Please enter a valid search term", "error")
		return redirect(url_for("view_categories"))
	# get businesses (users) with names matching search term:
	bizs = db_session.query(User).filter(User.biz_name.like(
		"%" + search_term + "%")).filter(Item.user_id != g.user.id).all()
	if not bizs:
		flash("Sorry, nothing matched your search.", "error")
		return redirect(url_for("view_categories"))
	else: 
		return render_template(
		"display_items.html", bizs=bizs, search_term=search_term, title="All Businesses Matching ", items=None)



######################################################
######################################################
######### These are the Trade functions #########
#####################################################
#####################################################

""" Open a trade request with another user """

@app.route("/open_request", methods=["GET", "POST"])
def open_request():
	if request.method == "GET":
		# get item id from url
		item_id = request.args.get("item")
		item = db_session.query(Item).filter_by(id=item_id).one()
	else:
		#instantiate new trade
		item_b = db_session.query(Item).filter_by(id=request.form["B_item_id"]).one()
		new_trade = Trade(
			open_date=datetime.datetime.utcnow()
			)
		db_session.add(new_trade)
		db_session.commit()
		

		#instantiate self as new participant
		new_participant_a = Participant(
			user_id=g.user.id, 
			item_id=int(request.form["A_item_id"]),
			trade_id=new_trade.id,
			total_qty=int(request.form["A_total_qty"]),
			current_qty=0, 
			requester=True	
			)
		db_session.add(new_participant_a)
		db_session.commit()


		#instantiate other person as new participant
		new_participant_b = Participant(
			user_id=item_b.user.id,
			item_id=int(request.form["B_item_id"]),
			trade_id=new_trade.id,
			total_qty=int(request.form["B_total_qty"]),
			current_qty=0,
			requester=False
			)
		db_session.add(new_participant_b)
		db_session.commit()

		flash("Your trade with " + item_b.user.biz_name + " was successfully requested.")
		return redirect(url_for('home'))
	# get entire item from DB
	return render_template("open_request.html", item=item)


""" Get notifications for any new trade requests """

def get_notifications():
	notifications = db_session.query(Participant).filter_by(user_id=g.user_id, requester=False, confirm=None).all()

	all_my_trades = db_session.query(Participant).filter_by(user_id=g.user_id, requester=True).all()

	new_confirms = [participant for participant in all_my_trades if participant.trade.participants[1].confirm == True]

	print new_confirms, "MLAHHCHCHHCHCHCHCHCHHCH"

	return notifications, new_confirms




""" Accept trade request"""

@app.route("/accept_trade/<int:id>", methods=["GET"])
def accept_trade(id):
	yes_participant = Participant.query.get(id)
	trade_partner = yes_participant.trade.participants[0].user.email
	yes_participant.confirm = True
	db_session.add(yes_participant)
	db_session.commit()
	flash("Trade accepted! Email " + trade_partner + " to confirm details.")
	return redirect("/home")



""" Refuse trade request """
@app.route("/refuse_trade", methods=["POST"])
def refuse_trade():
	pass

######################################################
######################################################
######### These are the Trade functions #########
#####################################################
#####################################################

@app.route("/manage_trades")
def manage_account():
	pass



if __name__ == "__main__":
	app.run(debug = True)
