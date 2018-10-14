#C:\Users\JakeDesktop\OneDrive\Python\GMBV6.py
#C:\Users\JakeLaptop\Desktop\OneDrive\Python\GMBV6.py
#FIX TOKEN ACCESS

import requests
import time
import datetime

botCall = '!bot'
helpCall = '!help'
nameCall = '!names'
request_params = {'token': "xGP1VqL0vAYKgBdNNE5az5MbLySz2e84wmLUJEJM"}


help_message = """
	Hey! To get my attention use this format!

	!bot meal name

	If you forget your name, use !names
	"""

#These lists hold names of those who want leftovers saved for each meal. Set to be wiped after the cutoff for dinner.
lunch_list = []
dinner_list = []
command_list = ['start']
message_log = []
initialize = 0
last_message_id = ''

#Used to make sure fake names or nicknames are not put onto the lists. Keeps things consistent for chef.
unadjusted_member_list = ["Jacob", "Carson", "Brendon","Petra","Wasserman","Thomas","Phan", "Harrison","Anderson","Lauerman","Amir","Evan","Nikko","Andrew","Fragasso","Quinn","Austin","Bryce","Yuhao","Karim","Binns","Blake","Josh","Peyton","Robert","Kris","Gabe","Justin","Luke","Bryce","Will","Aidan","Garrett","BJ","Steve","Deven","YenWen","Matthew","Nico", "Nussbaum","Ben","Sam","Owen","Javier","Rodrigo","Phelan", "Ryan","Jared","Howard","Colton","Dustin","Ari","Ed","Lampkin","Robi","Zach","JHerbruger","Kevin","Aune","Paul","Will","Cole", "Kelvin","Hytrek","Spencer","Tim"]
member_list = [entry.lower() for entry in unadjusted_member_list]

#Adjustable times for cutoffs, depending on meal type and chef requests
now = datetime.datetime.now()
lunch_cutoff_time = now.replace(hour =10, minute = 39, second = 30, microsecond = 0)
dinner_cutoff_time = now.replace(hour = 21, minute = 40, second = 0, microsecond = 0)	
reset_time = now.replace(hour = 23, minute = 47, second = 00, microsecond = 0)

#Method called to push message to GroupMe chat
def message_send (to_send):
	request_params = {'token': "xGP1VqL0vAYKgBdNNE5az5MbLySz2e84wmLUJEJM"}
	response = requests.get('https://api.groupme.com/v3/groups/43302265/messages', params = request_params)
	if (response.status_code == 200):
		response_messages = response.json()['response']['messages']
		post_params = { 'bot_id' : '6f8d34b8f636d81ff35d7d283c', 'text': to_send } 
		requests.post('https://api.groupme.com/v3/bots/post', params = post_params)
	
def time_comparator (now, lunch_cutoff_time, dinner_cutoff_time,lastMessage):
	if now < lunch_cutoff_time:
		time_status =  'morning'
		list_sorter(time_status,lastMessage)
		#add to lunch list
	elif (now > lunch_cutoff_time) & (now < dinner_cutoff_time):
		time_status = 'afternoon'
		list_sorter(time_status,lastMessage)
		#add to dinner list
	elif now > dinner_cutoff_time:
		message_send("You missed the last deadline! Check the fridge for leftovers and try again tomorrow!")
		#add to neither list
	else:
		pass

def list_sorter(time_status,lastMessage):
	if(time_status == 'morning'):
		string_parser(lastMessage)
	elif(time_status == 'afternoon'):
		string_parser(lastMessage)
	else:
		#oof
		pass

def string_parser(user_input):
	text = user_input.replace(" ","").lower()
	if "!botlunch" in text:
		text = text[9:]
		if text in member_list:
			match_index = [i for i, s in enumerate(member_list) if text in s]
			member_name = unadjusted_member_list[match_index[0]]
			if member_name not in lunch_list:
				lunch_list.append(member_name)
				print(str('Current lunch list ' + str(lunch_list)))
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
				message_send('Gotcha ' + member_name + ' you are on the dinner list!')		
				print(str('Current dinner list ' + str(dinner_list)))
			else:
				message_send("You're already on the dinner list " + member_name +"!")
		else:
			message_send('Name not recognized, use !names if you forgot your assigned name!')
	else:
		message_send("That's not a command, use !help if you don't remember the commands!")


#Params should be listed as variable request_params, which is globally defined, but cannot function in the while loop.
while True:
	now = datetime.datetime.now()
	if now > reset_time:
		#print('reset_time1')
		lunch_list.clear()
		dinner_list.clear()
	
	response_messages = requests.get('https://api.groupme.com/v3/groups/43302265/messages', params = {'token': "xGP1VqL0vAYKgBdNNE5az5MbLySz2e84wmLUJEJM"}).json()['response']['messages']
	if initialize == 0:
		print('initialize')
		initialize += 1
	else:
		try:
			latestId = response_messages[0]['id']
			if response_messages[0]['name'] == 'ThotBot':
				continue
			if latestId != last_message_id:
				last_message_id = latestId
				lastMessage = response_messages[0]['text']
				if lastMessage == '!help':
					message_send(help_message)
				elif lastMessage == '!names':
					message_send(str(unadjusted_member_list))					
				else:
					time_comparator(now, lunch_cutoff_time, dinner_cutoff_time, lastMessage)
				#print(str(lastMessage + ' sent by ' + response_messages[0]['name']))
		except(IndexError):
			print('No Messages In Chat')

	


	


