# GroupMeBot created by Jacob Madian
# This program was created to automate the process of allocating leftover food in a house of 40 people
# In the past, requests for leftover food have been made by writing your name on a whiteboard located in the kitchen
# As people forget to sign up before they leave, a large amount of people consistently ask for somebody to write their name on the board
# This code uses a GroupMe chat to automate this feature and display active lists for lunch and dinner requests
# A raspberry pi is consistently running this code in the kitchen attached to a monitor for visual access, and resets all request lists at a specified time

import requests
import time
import datetime
import os
from texttable import Texttable

# Commands used to activate bot
botCall = '!bot'
helpCall = '!help'
nameCall = '!names'

# Opens the token file, allowing for outgoing messages
with open("/home/pi/LatePlateBot/Token.txt","r") as file: bot_token = file.read()
request_params = {'token': bot_token}

# Lambda function for resetting terminal window
clear = lambda : os.system('reset')
clear()

help_message = """
	Hey! To get my attention use this format!

	!bot meal full name

	If you forget your assigned name, use !names PC(insert number here)

	!names PC16

	As an example
	"""

# These lists hold names of those who want leftovers saved for each meal. Set to be wiped after the reset time: reset_time.
lunch_list = []
dinner_list = []
initialize = 0
last_message_id = ''

# Table creation and initialization
lunch_output_table = Texttable()
dinner_output_table = Texttable()
dinner_output_table.add_row([['        Dinner         ']])
lunch_output_table.add_row([['         Lunch         ']])
lunch_output_table.set_cols_align("c")
dinner_output_table.set_cols_align("c")

# Used to make sure fake names or nicknames are not put onto the lists. Keeps things consistent for chef.
unadjusted_member_list = open("/home/pi/LatePlateBot/Member_List.txt").read().splitlines()
member_list = [entry.replace(" ","").lower() for entry in unadjusted_member_list]

# List subdivision to avoid extremely long lists sent to chat
PC18_names = unadjusted_member_list[:18]
PC17_names = unadjusted_member_list[18:40]
PC16_names = unadjusted_member_list[40:61]
PC15_names = unadjusted_member_list[61:84]

# Adjustable times for cutoffs, depending on meal type and chef requests
lunch_cutoff_time = datetime.datetime.now().replace(hour =23, minute = 39, second = 30, microsecond = 0)
dinner_cutoff_time = datetime.datetime.now().replace(hour = 23, minute = 40, second = 0, microsecond = 0)	
reset_time = datetime.datetime.now().replace(hour = 23, minute = 47, second = 00, microsecond = 0)

# Method called to push message to GroupMe chat
def message_send (to_send):

	if last_response_code == 200:
		requests.post('https://api.groupme.com/v3/bots/post', params = { 'bot_id' : '6f8d34b8f636d81ff35d7d283c', 'text': to_send })

# Sorts message to various conditions depending on time relative to cutoffs
def time_comparator (now, lunch_cutoff_time, dinner_cutoff_time,lastMessage):

	if now <= lunch_cutoff_time:
		string_parser(lastMessage)

	elif (now > lunch_cutoff_time) & (now <= dinner_cutoff_time):
		if "!botlunch" in lastMessage.replace(" ","").lower():
			message_send("You're to late for lunch plates! Check the fridge for leftovers and try again tomorrow!")
		else:
			string_parser(lastMessage)
	else:
		message_send("You missed the last deadline! Check the fridge for leftovers and try again tomorrow!")

# Message creation and list appending, as well as table clearing and redrawing
def string_parser(user_input):
	text = user_input.replace(" ","").lower()
	if "!botlunch" in text:
		text = text[9:]
		if text in member_list:
			match_index = [i for i, s in enumerate(member_list) if text in s]
			member_name = unadjusted_member_list[match_index[0]]
			if member_name not in lunch_list:
				lunch_list.append(member_name)
				#(str('Current lunch list')
				lunch_output_table.add_row([[str(member_name)]])
				clear()
				print(lunch_output_table.draw())
				print(dinner_output_table.draw())
				message_send('Gotcha ' + member_name + ' you are on the lunch list!')
			else:
				message_send("You're already on the lunch list " + member_name +"!")
		else:
			message_send('Name not recognized, use !names if you forgot your assigned name!')
	elif "!botdinner" in text:
		text = text[10:]
		if text in member_list:
			match_index = [i for i, s in enumerate(member_list) if text in s]
			member_name = unadjusted_member_list[match_index[0]]
			if member_name not in dinner_list:
				dinner_list.append(member_name)
				#print(str('Current dinner list ' + str(dinner_list)))
				dinner_output_table.add_row([[str(member_name)]])
				clear()
				print(lunch_output_table.draw())
				print(dinner_output_table.draw())
				message_send('Gotcha ' + member_name + ' you are on the dinner list!')
			else:
				message_send("You're already on the dinner list " + member_name +"!")
		else:
			message_send('Name not recognized, use !names if you forgot your assigned name!')
	else:
		message_send("That's not a command, use !help if you don't remember the commands!")

#Function sorts which grouping of names to send to avoid clutter in main code body
def name_selection(user_input):
	if "pc18" in user_input.lower():
		message_send(str(PC18_names))
	elif "pc17" in user_input.lower():
		message_send(str(PC17_names))
	elif "pc16" in user_input.lower():
		message_send(str(PC16_names))
	elif "pc15" in user_input.lower():
		message_send(str(PC15_names))
	else:
		message_send("Try again but make sure to include PC with your year following it!")

while True:
	time.sleep(.5)
	now = datetime.datetime.now()
	if now > reset_time:
		lunch_list.clear()
		dinner_list.clear()
		clear()
	try:
		response = requests.get('https://api.groupme.com/v3/groups/43302265/messages', params = {'token': bot_token})
		response_messages = response.json()['response']['messages']
		last_response_code = response.status_code
		try:
			assert last_response_code == 200
		except AssertionError:
			print("Bad response Code: " + last_response_code)
	except TypeError:
		continue

	if initialize == 0:
		print('initialize')
		initialize += 1
	else:
		try:
			message = response_messages[0]
			latestId = message['id']
			if message['name'] == 'ThotBot':
				continue
			if latestId != last_message_id:
				last_message_id = latestId
				lastMessage = message['text']
				if lastMessage == '!help':
					message_send(help_message)
				elif "!names" in lastMessage.lower():
					name_selection(lastMessage)
				else:
					time_comparator(now, lunch_cutoff_time, dinner_cutoff_time, lastMessage)
		except(IndexError):
			print('No Messages In Chat')

	


	


