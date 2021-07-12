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
    # Nah ini menu utamany
    a = 1+1
    return "abd {}".format(a)

if  __name__ =="__main__":
    app.run()