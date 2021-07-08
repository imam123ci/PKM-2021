# FLASK TEST
# To Try, rename this file to app.py
# ----------------------------------
# Try Flask For the first Time
# ----------------------------------


from flask import Flask, escape, request

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'