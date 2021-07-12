# FLASK API
# To Try, rename this file to app.py
# ----------------------------------
# Try Flask For generating REST API
# ----------------------------------

# save this as app.py
from flask import Flask, escape, request

app = Flask(__name__)

@app.route('/')
def satu():
    # Nah ini menu utamanya
    return "Menu kedua"

@app.route('/<userid>')
def dua(userid):
    # predict buzzer her
    # set likelihood of being buzzer
    # return following prediction\
    return "{} : buzzer".format(userid)
