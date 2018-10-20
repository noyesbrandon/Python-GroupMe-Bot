"""
GroupMeBot created by Jacob Madian
Open Readme.txt for description and functionality notes
"""

import time
import datetime
import os
import requests
from texttable import Texttable

# Commands used to activate bot
bot_call = '!bot'
help_call = '!help'
name_call = '!names'
bot_id = '6f8d34b8f636d81ff35d7d283c'
bot_link = 'https://api.groupme.com/v3/bots/post'
chat_link = 'https://api.groupme.com/v3/groups/43302265/messages'

# Paths for Raspberry Pi
# token_path = "/home/pi/LatePlateBot/Token.txt"
# member_path = "/home/pi/Git/LatePlateBot/Python-GroupMe-Bot/Member_List.txt"

# Paths for Laptop work
token_path = "C:/Users/JakeLaptop/Desktop/Token.txt"
member_path = "C:/Users/JakeLaptop/Desktop/Member_List.txt"

help_message = """
Hey! To get my attention use this format!

!bot meal full name

If you forget your assigned name, use !names PC(insert number here)

!names PC16
"""

# Opens the token file, allowing for outgoing messages
with open(token_path, "r") as file: bot_token = file.read()
request_params = {'token': bot_token}

# Lambda function for resetting terminal window "reset for Raspberry Pi, cls for PC"
#clear = lambda: os.system('reset')
clear = lambda: os.system('cls')
clear()

# Lists hold names of those who want leftovers. Set to be wiped after the reset time: reset_time.
lunch_list = []
dinner_list = []
initialize = 0
last_message_id = ''

# Table creation and initialization
lunch_output_table = Texttable()
dinner_output_table = Texttable()

# Extra spaces to allow for large names to not be on multiple lines
dinner_output_table.add_row([['        Dinner         ']])
lunch_output_table.add_row([['         Lunch         ']])
lunch_output_table.set_cols_align("c")
dinner_output_table.set_cols_align("c")

# Used to make sure fake names are not put onto the lists.
unadjusted_member_list = open(member_path, "r").read().splitlines()
member_list = [entry.replace(" ", "").lower() for entry in unadjusted_member_list[1:]]


# List subdivision to avoid extremely long lists sent to chat
PC15_names = unadjusted_member_list[1:24]
PC16_names = unadjusted_member_list[25:46]
PC17_names = unadjusted_member_list[47:69]
PC18_names = unadjusted_member_list[70:]

# Adjustable times for cutoffs, depending on meal type and chef requests
lunch_cutoff_time = datetime.datetime.now().replace(hour=23, minute=39, second=30)
dinner_cutoff_time = datetime.datetime.now().replace(hour=23, minute=40, second=0)
reset_time = datetime.datetime.now().replace(hour=23, minute=47, second=0)

# Method called to push message to GroupMe chat
def message_send(to_send):
    """
    This function pushes to_send text to GroupMe chat through bot account
    """

    if last_response_code == 200:
        requests.post(bot_link, params={'bot_id':bot_id, 'text':to_send})

# Sorts message to various conditions depending on time relative to cutoffs
def time_comparator(current_time, lunch_cutoff, dinner_cutoff, last_message):
    """
    Function determines time condition and uses
    to intercept illegal requests from users

    The if statement presumes the request is before
    any cutoff time, so it should pass without trouble

    The elif is determining if a lunch request has been
    made after the cutoff time, otherwise (dinner request)
    it passes the request through

    If neither of these conditions are met, it must be after
    the dinner cutoff time, at which no requests are accepted
    """
    if now <= lunch_cutoff_time:
        string_parser(last_message)

    elif (now > lunch_cutoff_time) & (now <= dinner_cutoff_time):
        if "!botlunch" in last_message.replace(" ", "").lower():
            message_send("You're to late for lunch plates! Check the fridge!")
        else:
            string_parser(last_message)
    else:
        message_send("You missed the last deadline! Check the fridge!")

# Message creation and list appending, as well as table clearing and redrawing
def string_parser(user_input):
    """
    This is arguably the most complicated function...
    It filters the input through removing spaces and lowering text

    Then, it figures out which meal the user is inquiring about.
    After, the command text is removed from the user input
    only leaving the user's name.

    This is then checked against the member list to confirm the identity
    at which point the location of the name is found in the unadjusted list.

    If the name is not currently on the meal specific list, then it is added,
    and the new table is drawn in the output.
    """
    input_filtered = user_input.replace(" ", "").lower()
    if "!botlunch" in input_filtered:
        # Removing bot meal call to only retain users name
        potential_name = input_filtered[len("!botlunch"):]
        if potential_name in member_list:
            match_index = [i for i, s in enumerate(member_list) if potential_name in s]
            member_name = unadjusted_member_list[match_index[0]+1]
            if member_name not in lunch_list:
                lunch_list.append(member_name)
                lunch_output_table.add_row([[str(member_name)]])
                clear()
                print(lunch_output_table.draw())
                print(dinner_output_table.draw())
                message_send('Gotcha ' + member_name + ' you are on the lunch list!')
            else:
                message_send("You're already on the lunch list " + member_name +"!")
        else:
            message_send('Name not recognized, use !names if you forgot your assigned name!')
    elif "!botdinner" in input_filtered:
        # Again, removing bot meal call to retain users name
        potential_name = input_filtered[len("!botdinner"):]
        if potential_name in member_list:
            match_index = [i for i, s in enumerate(member_list) if potential_name in s]
            member_name = unadjusted_member_list[match_index[0]+1]
            if member_name not in dinner_list:
                dinner_list.append(member_name)
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

# Function sorts which grouping of names to send to avoid clutter in main code body
def name_selection(user_input):
    """
    Function determines the PC the user is inquiring about
    then sends the list back to the GroupMe chat
    """

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
        response = requests.get(chat_link, params={'token': bot_token})
        response_messages = response.json()['response']['messages']
        last_response_code = response.status_code
        try:
            assert last_response_code == 200
        except AssertionError:
            print("Bad response Code: " + last_response_code)
    except TypeError:
        continue
    if initialize == 0:
        #print('initialize')
        initialize += 1
    else:
        try:
            message = response_messages[0]
            latestId = message['id']
            # Ignoring all messages sent by Bot
            if message['name'] == 'ThotBot':
                continue
            # Only new messages are filtered through
            if latestId != last_message_id:
                last_message_id = latestId
                latest_message = message['text']
                if '!help' in latest_message.lower():
                    message_send(help_message)
                elif "!names" in latest_message.lower():
                    name_selection(latest_message)
                else:
                    time_comparator(now, lunch_cutoff_time, dinner_cutoff_time, latest_message)
        except IndexError:
            print('No Messages In Chat')
            