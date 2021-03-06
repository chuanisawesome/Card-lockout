from flask import Flask
from flask import request
import yaml
import json
import sql
import psycopg2
import time

app = Flask( __name__ )

# connect to database makerspace
conn = psycopg2.connect("host=localhost dbname=makerspace user=postgres")
# open a cursor to perform database operations
cur = conn.cursor()

# @app.route("/")
# def welcome():

# adding user from form input
def add_user(card_id, uw_id, uw_netid, first_name, last_name):
	# searches table for existing users with any matching unique inputs, i.e. duplicates
	cur.execute("SELECT * FROM users WHERE card_id=%(card_id)s OR uw_id=%(uw_id)s OR uw_netid=%(uw_netid)s")
		% {'card_id': str(card_id), 'uw_id': str(uw_id), 'uw_netid': str(uw_netid)}
	# add user to table if no duplicates are found
	if len(cur.fetchall()) == 0:
		cur.execute("INSERT INTO users (card_id, uw_id, uw_netid, first_name, last_name) VALUES(%(card_id)s, %(uw_id)s, %(uw_netid)s, %(first_name)s, %(last_name)s)")
			% {'card_id': str(card_id), 'uw_id': str(uw_id), 'uw_netid': str(uw_netid), 'first_name': str(firstname), 'last_name': str(last_name)}
	# error, duplicates found
	else:

# removing user from form input
def remove_user(card_id, uw_id, uw_netid):
	# searches for user with a matching input
	cur.execute("SELECT * FROM users WHERE card_id=%(card_id)s OR uw_id=%(uw_id)s OR uw_netid=%(uw_netid)s")
		% {'card_id': str(card_id), 'uw_id': str(uw_id), 'uw_netid': str(uw_netid)}
	# if a user is found, remove from table
	if len(cur.fetchall()) == 1:
		cur.execute("DELETE FROM users")
		# move deleted user to new table?
	# error, no user found matching inputs
	else:
		
# editing user entry by form input
def edit_user(old_uw_id, card_id, uw_id, uw_netid, first_name, last_name):
	# gets id of user entry matching 
	cur.execute("SELECT id FROM users WHERE uw_id=%(uw_id)s") % {'uw_id': str(old_uw_id)}
	# if id is found update user entry
	if len(cur.fetchall()) == 1:
		id = cur.fetchall()[0]
		cur.execute("UPDATE users SET card_id=%(card_id)s, uw_id=%(uw_id)s, uw_netid=%(uw_netid)s, first_name=%(first_name)s, last_name=%(last_name)s WHERE id=%(id)s")
			% {'card_id': str(card_id), 'uw_id': str(uw_id), 'uw_netid': str(uw_netid), 'first_name': str(firstname), 'last_name': str(last_name), 'id': str(id)}
	# error, no id found so no update
	else:

# display all users
def display_users():
	table = "<table>"
	cur.execute("SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='users'")
	header = cur.fetchall()
	for column in header:
		table += "<th>" + str(column[3]) + "</th>"
	cur.execute("SELECT * FROM users")
	data = cur.fetchall()
	for row in data:
		table += "<tr>"
		for column in row:
			table += "<td>" + str(column) + "</td>"
		table += "</tr>"
	return table + "</table>"

# add membership to uw_id given card_id and type of membership
# expiration_date is only required if it is a main_door membership
def add_membership(card_id, type, expiration_date):
	pass

# display all memberships and allow removing one by selecting one
def remove_membership(card_id, type, expiration_date):
	pass

# edit details of a membership
def edit_membership(card_id, type, expiration_date):
	pass

# ban membership of uw_id given card_id and type of membership
# start_date is from time of form submission and end_date set by submitter
def ban_card(card_id, type, start_date, end_date):
	pass

# display list of all bans and allow unbanning by selecting one
def unban_card(card_id, type, start_date, end_date):
	pass

def add_card_reader():
	pass

def edit_card_reader():
	pass

def remove_card_reader():
	pass

def add_equipment_groups():
	pass

def edit_equipment_groups():
	pass

def remove_equipment_groups():
	pass

# checks card number for bans then for membership then if membership is expired
def card_swipe(card_id, card_reader):
	# given card_reader id get equipment type from card_readers table
	cur.execute("SELECT type FROM card_readers WHERE id=%(card_reader)s", {'card_reader': card_reader})
	if cur.rowcount > 0:
		type = cur.fetchall()[0][0]
		# given user's card_id get user's uw_id from users table
		cur.execute("SELECT uw_id FROM users WHERE card_id=%(card_id)s", {'card_id': card_id})
		if cur.rowcount > 0:
			uw_id = cur.fetchall()[0][0]
			# search memberships table for uw_id and equipment type and if found return expiration_date
			cur.execute("SELECT expiration_date FROM memberships WHERE uw_id=%(uw_id)s AND type=%(type)s ORDER BY expiration_date DESC", {'uw_id': uw_id, 'type': type})
			if cur.rowcount > 0:
				expiration_date = cur.fetchall()[0][0]
				if expiration_date > time.time():
					return 'GJ YOU IN'
					# call write_card_activity()
	else:
		return 'U FAILED'

# writes to table card_activity
def write_card_activity(uw_id, type, date, pass='0'):
	pass

# optional: show which equipment types a user is trained on
def show_trained_equipment(uw_id):
	pass

# optional: show all users trained on an equipment type
def show_trained_users(type):
	pass

if __name__ == '__main__':
	# read and return a yaml file (called 'config.yaml' by default) and give it
	# back as a dictionary
	with open( 'config.yaml' ) as f:
		config = yaml.load( f )

	app.debug = True
	app.run( host='0.0.0.0', port=config['serverPort'] )