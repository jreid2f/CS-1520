# Joseph Reidell
# Project 3: So You Think You Can Cater 
# CS 1520

from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

event_staff = db.Table('event_staff', db.Column('event_id', db.Integer, db.ForeignKey('event.id')), db.Column('staff_id', db.Integer, db.ForeignKey('staff.id')))

class Owner(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(80), unique=True)

	def __repr__(self):
		return '<Owner {}>'.format(repr(self.username))

class Staff(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(80), unique=True)
	staffers = db.relationship('Event', secondary=event_staff, backref=db.backref('eventStaffers', lazy='dynamic'))

	def __repr__(self):
		return '<Staff {}>'.format(repr(self.username))

class Customer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(80), unique=True)
	events = db.relationship('Event', backref='customers', lazy='dynamic')

	def __repr__(self):
		return '<Customer {}>'.format(repr(self.username))

class Event(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80))
	date = db.Column(db.Date())
	customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
	events = db.relationship('Staff', secondary=event_staff, backref=db.backref('events', lazy='dynamic'))

	def __repr__(self):
		return '<Event {}>'.format(repr(self.title))