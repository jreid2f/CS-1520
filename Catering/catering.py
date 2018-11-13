# Joseph Reidell
# Project 3: So You Think You Can Cater 
# CS 1520

from flask import Flask, render_template, redirect, url_for, request, session, flash
from models import Owner, Staff, Customer, Event, db
from datetime import date
#from flask_debugtoolbar import DebugToolbarExtension
import os

app = Flask(__name__)
#app.debug = True

app.config.update(dict(
	DEBUG=True,
	SECRET_KEY='development key',
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'catering.db')
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

db.init_app(app)

#toolbar = DebugToolbarExtension(app)

@app.cli.command('initdb')
def initdb_command():
	"""Creates the database tables."""
	db.drop_all()
	db.create_all()
	own = Owner(username="owner", password="pass")
	db.session.add(own)
	db.session.commit()
	print('Initialized the database.')

@app.route('/')
def default():
	return redirect(url_for("login"))

@app.route('/login', methods=['GET', 'POST'])
def login():
	session['logged_in'] = False
	if request.method == 'POST':
		if Owner.query.filter_by(username=request.form["user"], password=request.form["pass"]).first() != None:
			session['logged_in'] = True
			return redirect(url_for("owner"))
		elif Staff.query.filter_by(username=request.form["user"], password=request.form["pass"]).first() != None:
			session['logged_in'] = True
			return redirect(url_for("staffer", username=request.form["user"]))
		elif Customer.query.filter_by(username=request.form["user"], password=request.form["pass"]).first() != None:
			session['logged_in'] = True
			return redirect(url_for("customer", username=request.form["user"]))
		else:
			flash('Sorry, this profile does not exist! Try creating a customer account!')
	return render_template("login.html")

@app.route("/owner", methods=['GET', 'POST'])
def owner():
	events = Event.query.all()
	return render_template("owner.html", events = events)

@app.route('/new_customer', methods=['GET', 'POST'])
def customer_account():
	if request.method=="POST":
		custom = Customer(username=request.form["username"], password=request.form["password"])
		db.session.add(custom)
		db.session.commit()
		flash("Your customer account is created!")
		return redirect(url_for("login"))
	return render_template("customer_account.html")

@app.route('/new_staffer', methods=['GET', 'POST'])
def staffer_account():
	if request.method=="POST":
		s = Staff(username=request.form["username"], password=request.form["password"])
		db.session.add(s)
		db.session.commit()
		flash("The new staff account is created!")
		return redirect(url_for("owner"))
	session['logged_in'] = True
	return render_template("staffer_account.html")

@app.route('/cancel-event', methods=['GET', 'POST'])
def cancel_event():
	if request.method=="POST":
		event_title=request.form["title"]
		curr_date=request.form["date"]
		year, month, day=curr_date.split('-')
		event_date=date(int(year),int(month),int(day))
		db.session.delete(Event.query.filter_by(title=event_title, date=event_date).first())
		db.session.commit()
		flash("Your event was cancelled")
		session['logged_in'] = True
	return render_template("cancel_event.html")

@app.route("/customer/<username>", methods=["GET", "POST"])
@app.route("/customer/", methods=["GET", "POST"])
def customer(username=None):
	user = username
	custom = Customer.query.filter_by(username=user).first()
	events = Event.query.filter_by(customer_id = custom.id).all()
	if request.method=="POST":
		user = username
		curr_date = request.form['event_date']
		year, month, day = curr_date.split('-')
		event_date = date(int(year), int(month), int(day))
		if Event.query.filter_by(date=event_date).first() == None:
			eve = Event(title=request.form["event_title"], date=event_date, customers = custom)
			db.session.add(eve)
			db.session.commit()
			flash("Your event was created!")
		else:
			flash("This day is already booked! Sorry!")
	session['logged_in'] = True
	return render_template("customer.html", username = user, events = events)

@app.route('/staffer/<username>', methods=["GET", "POST"])
def staffer(username=None):
	staff = Staff.query.filter_by(username=username).first()
	events = Event.query.all()
	signup = []
	avaliable = []
	for event in events:
		if event in staff.events:
			signup.append(event)
		else:
			avaliable.append(event)
	if request.method=="POST":
		signup_event = request.form["event"]
		event = Event.query.filter_by(title=signup_event).first()
		event.eventStaffers.append(staff)
		db.session.commit()
		flash("Event has been assigned! Reload the page to see your list!")
	return render_template("staffer.html", staff=staff, signup=signup, avaliable=avaliable)

@app.route('/logout/')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('login'))
	
if __name__ == "__main__":
	app.run()

    
