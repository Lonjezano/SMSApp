# Your code goes here
from flask import Flask, request
import africastalking
import os

app = Flask(__name__)
username = "sandbox"
api_key = ""
africastalking.initialize(username, api_key)
sms = africastalking.SMS


@app.route('/', methods=['POST', 'GET'])


def ussd_callback():
    global response
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")
    sms_phone_number = []
    sms_phone_number.append(phone_number)

    #ussd logic
    if text == "":
        #main menu
        response = "CON What would you like to do?\n"
        response += "1. Report a fault\n"
        response += "2. Apply fro a new system\n"
        response += "3. Apply for system maintenance\n"
        response += "4. Apply for system relocation"
    elif text == "1":
        #sub menu 1
        response = "CON What would you like report\n"
        response += "1. Output power failure\n"
        response += "2. System shutdown\n"
        response += "3. AC input failure\n"
        response += "4. Account balance\n"
        response += "5. PC voltage too low\n"
        response += "6. Batteries run out too fast\n"
        response += "7. System offline\n"
        response += "8. Other (Specify)"
    elif text == "2":
        response = "CON What system would you like to apply for\n"
        response += "1. Hybrid system\n"
        response += "2. Grid-tie system\n"
        response += "3. Off-Grid system\n"
        response += "4. Other (Specify)"
    elif text == "3":
        response = "CON What system would you like to maintain\n"
        response += "1. PC Panels cleaning\n"
        response += "2. Battery replacement\n"
        response += "3. Battery cleaning\n"
        response += "4. DC Isolator replacement\n"
        response += "5. Other (Specify)"
    elif text == "4":
        response = "CON Where would you like to relocate\n"
        response += "1. Current location\n"
        response += "2. New location"
    elif text == "1*1":
        #ussd menus are split using *
        account_number = "1243324376742"
        response = "END Your account number is {}".format(account_number)
    elif text == "1*2":
        account_balance = "100,000"
        response = "END Your account balance is USD {}".format(account_balance)
    elif str(text).endswith("0"):
        text = ""
        ussd_callback()
    else:
        response = "END Invalid input. Try again."

    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.environ.get('PORT'))


