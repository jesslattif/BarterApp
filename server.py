
from flask import Flask, render_template, redirect, request, session, url_for
import model
from model import User, Item, Participant, Trade, session as db_session

app  = Flask(__name__)
app.secret_key ="RZEB`YhM#EO|rhVWx~|U9,iYauiv l7B1t=ntDr7l-W&aM}JS2%"


"""Index""" #this is the main page everyone sees when navigating to URL

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

@app.route("/", methods=["POST"])
def save_new_user(): 
	new_user = User(email=request.form["email"], password=request.form["password"], age=request.form["age"], zipcode=request.form["zipcode"])#new instance of class "User", fields filled in from web form
	db_session.add(new_user) #add & commit new user
	db_session.commit()
	user_email = new_user.email
	return render_template("new_user.html", user_email=user_email)


"""Log-in"""

@app.route("/log_in")
def log_in():
	return render_template("log_in.html")


"""Authenticate User"""

@app.route("/authenticate", methods=["POST"])
def authenticate(): # authenticate user
	email = request.form['email']
	password = request.form['password']
	user = db_session.query(User).filter_by(email=email, password=password).first() #checks for user in db

	if not user: #redirect to log-in if info not correct
		print "FAILED LOGIN"
		return redirect("/log_in")

	print "SUCCEEDED" 
	session["user_id"] = user.id #set session
	return redirect("/my_barter_profile") #redirects to user's movie ratings page for unique user id


"""Go to user's homepage"""

@app.route("/my_barter_profile")
def go_to_homepage():
	user_id = session.get("user_id") #gets user ID from current session
	if not user_id: # redirects to log-in if no user ID session
		return redirect("/log_in")
	user = db_session.query(User).filter_by(id = user_id).first()
	user_name = user.first_name

	return render_template("my_barter_profile.html", user_name = user_name)


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
		return redirect("/log_in")

	user = db_session.query(User).get(user_id) #gets user object based on user_id
	items = user.items 
	return render_template("manage_items.html", user_items =items, user=user)


"""Add new item"""
@app.route('/add_item')
def add_item():
	user_id = session.get("user_id")
	if not user_id: # redirects to log-in if no user ID session
		return redirect("/log_in")
	return render_template("add_item.html", user=user_id)


@app.route("/insert_item", methods=["POST"])
def insert_item():
	user_id = session.get("user_id")
	if not user_id: # redirects to log-in if no user ID session
		return redirect("/log_in")
	user = db_session.query(User).get(user_id)#gets user
	name_string = str(request.form["name"]) #takes in new item name as a string
	descr_string = str(request.form["description"]) #takes in new item description as a string 
	new_name = Item(name=name_string, description=descr_string) #creates new item object from user's input
	new_name.user = user #attach item object to user object
	
	db_session.commit()
	return redirect("/manage_items")


"""Edit item name"""

@app.route("/edit_item/<int:id>", methods=["GET"])
def edit_item(id):
	user_id = session.get("user_id")
	if not user_id: # redirects to log-in if no user ID session
		return redirect("/log_in")
	item = db_session.query(Item).get(id)
	return render_template("/edit_item.html", item=item)


"""Update edited item name"""

@app.route("/update_item", methods=["POST"])
def update_item():
	user_id = session.get("user_id")
	if not user_id: # redirects to log-in if no user ID session
		return redirect("/log_in")
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
		return redirect("/log_in")
	item = db_session.query(Item).get(id)
	return render_template("/edit_description.html", item=item)

"""Update Item Description"""

@app.route("/update_description", methods=["POST"])
def update_description():
	user_id = session.get("user_id")
	if not user_id: # redirects to log-in if no user ID session
		return redirect("/log_in")
	user = db_session.query(User).get(user_id) #gets user id
	item = db_session.query(Item).get(request.args.get("id")) #gets item id
	descr_string = str(request.form["description"]) #takes in new description as string
	item.description = descr_string
	db_session.commit()
	return redirect("/manage_items")

"""Delete Item"""

@app.route("/delete_item")
def delete_item():
	user_id = session.get("user_id")
	if not user_id: # redirects to log-in if no user ID session
		return redirect("/log_in")
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
		return redirect("/log_in")
	pass


@app.route("/find_partners")
def find_partners():
	user_id = session.get("user_id")
	if not user_id: # redirects to log-in if no user ID session
		return redirect("/log_in")
	pass

@app.route("/open_request")
def open_request():
	user_id = session.get("user_id")
	if not user_id: # redirects to log-in if no user ID session
		return redirect("/log_in")
	pass


@app.route("/manage_account")
def manage_account():
	pass




if __name__ == "__main__":
	app.run(debug = True)
