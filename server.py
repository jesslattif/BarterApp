
from flask import Flask, render_template, redirect, request, session, url_for
import model
from model import User, Item, Participant, Trade, session as db_session

app  = Flask(__name__)
app.secret_key ="RZEB`YhM#EO|rhVWx~|U9,iYauiv l7B1t=ntDr7l-W&aM}JS2%"


"""Index""" #this is the main page everyone sees when navigating to URL

@app.route("/")
def index():
	return render_template("index.html")

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
	return redirect("/my_homepage") #redirects to user's movie ratings page for unique user id


"""Go to user's homepage"""

@app.route("/my_barter_profile")
def go_to_homepage():
	user_id = session.get("user_id") #gets user ID from current session
	if not user_id: # redirects to log-in if no user ID session
		return redirect("/log_in")
	return render_template("my_barter_profile.html")






if __name__ == "__main__":
	app.run(debug = True)
