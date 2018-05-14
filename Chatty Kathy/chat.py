# Joseph Reidell
# Project 4: Chatty Kathy 
# CS 1520

from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify, abort, _app_ctx_stack
from models import db, Users, Messages, Chatroom
from datetime import date, datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from json import loads, dumps
import os

app = Flask(__name__)
#app.debug = True

app.config.update(dict(
	DEBUG=True,
	SECRET_KEY='development key',
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'chat.db')
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

db.init_app(app)

#toolbar = DebugToolbarExtension(app)

@app.cli.command('initdb')
def initdb_command():
	"""Creates the database tables."""
	db.drop_all()
	db.create_all()
	print('Initialized the database.')

def get_user_id(username):
	ref = Users.query.filter_by(username=username).first()
	return ref.user_id if ref else None

def get_room_id(name):
	ref = Chatroom.query.filter_by(name=name).first()
	return ref.chat_id if ref else None

def check_datetime(time):
	if isinstance(time, datetime.datetime):
		return time.isoformat()

	raise TypeError('Unknown error type')

@app.route('/')
def default():
	return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if session.get('user_id'):
		return redirect(url_for('chatroom'))
	else:
		if request.method == 'POST':
			username = request.form['username']
			password = request.form['password']

			user = Users.query.filter_by(username=username).first()

			if user is None:
				error = 'Invalid Username'
			elif not user.password == password:
				error = 'Invalid Password'
			else:
				flash('{} was logged in'.format(username))
				session['user_id'] = user.user_id
				session.pop('room_id', None)
				return redirect(url_for('chatroom'))
		return render_template('login.html', error=error)

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
	error = None
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if get_user_id(username) is not None:
			error = 'Sorry! This username was taken!'
		else:
			user = Users(username=username, password=password)
			db.session.add(user)
			db.session.commit()
			flash('Your new account was created!')
			return redirect(url_for('login'))
	return render_template('create_user.html', error=error)

@app.route('/create_chatroom', methods=['GET', 'POST'])
def create_chatroom():
	error = None
	if request.method == 'POST':
		chat_name = request.form['username']
		user = Users.query.filter_by(user_id=session['user_id']).first()
		if get_room_id(chat_name) is not None:
			error = 'This chatroom name is already taken!'
		else:
			room = Chatroom(name=chat_name, create_id=user.user_id)
			db.session.add(room)
			db.session.commit()
			flash('New chatroom {} was created!'.format(chat_name))
			return redirect(url_for('chatroom'))
	return render_template('create_chatroom.html', error=error)

@app.route('/join_chatroom', methods=['GET', 'POST'])
def chatroom():
	error=None
	if request.method == 'POST':
		delete_room = request.form['delete']
		if delete_room:
			chatroom = Chatroom.query.filter_by(chat_id=delete_room).first()
			if chatroom.create_id == session['user_id']:
				flash('Chatroom {} was successfully deleted!'.format(chatroom.name))
				db.session.delete(chatroom)
				db.session.commit()
			else:
				error = 'This chatroom cannot be deleted because you did not create it!'
		else:
			error = 'This chatroom no longer exists!'
	chatrooms = Chatroom.query.all()
	return render_template('join_chatroom.html', chatrooms=chatrooms, error=error)

@app.route('/chatty_room/<name>', methods=['GET', 'POST'])
def chatty_room(name):
	chatty = Chatroom.query.filter_by(name=name).first()
	if session.get('room_id'):
		if session['room_id'] == None or session['room_id'] == chatty.chat_id:
			session['room_id'] = chatty.chat_id
			msg = Messages.query.filter(Messages.room_id==session['room_id']).all()
			return render_template('chatty_room.html', roomName=name, post=msg)
		else:
			old = Chatroom.query.filter_by(chat_id=session['room_id']).first()
			flash('Sorry! You can only be in one chatroom at a time!')
			return redirect(url_for('chatty_room', name=old.name))
	else:
		session['room_id'] = chatty.chat_id
		msg = Messages.query.filter(Messages.room_id==session['room_id']).all()
		return render_template('chatty_room.html', roomName=name, post=msg)

@app.route('/leave_chatroom', methods=['GET', 'POST'])
def leave_chatroom():
	current = Chatroom.query.filter_by(chat_id=session['room_id']).first()
	flash('You left the chatroom: {}. You may now join a different chatroom!'.format(current.name))
	session.pop('room_id', None)
	return redirect(url_for('chatroom'))


@app.route('/setMessage', methods=['POST'])
def setMessage():
	text = request.json
	current = Users.query.filter_by(user_id=session['user_id']).first()
	msg = Messages(message=text['msg'], post_date=datetime.now(), send_id=session['user_id'], room_id=session['room_id'], post_msg=current.username)
	db.session.add(msg)
	db.session.commit()
	return render_template('chatty_room.html')

@app.route('/getMessage', methods=['GET'])
def getMessage():
	current = Chatroom.query.filter_by(chat_id=session['room_id']).first()
	if current:
		msg = Messages.query.with_entities(Messages.message, Messages.post_msg).filter((Messages.room_id==session['room_id']) & (Messages.post_date.between((datetime.now()-timedelta(seconds=1)), datetime.now()))).all()
		return dumps(msg)
	else:
		flash('Sorry this room was deleted! Please join another room!')
		session.pop('room_id', None)
		return 'Please leave this room as soon as you as can! I would like to go home!'

@app.route('/logout/')
def logout():
	flash('You were logged out')
	session.pop('user_id', None)
	session.pop('room_id', None)
	return redirect(url_for('login'))
	
if __name__ == "__main__":
	app.run(debug=True)
