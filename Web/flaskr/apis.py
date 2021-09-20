# api blueprint
import random

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, make_response, jsonify
)
from flaskr.mongodb import get_twitter_timeline, get_twitter_users
from flaskr.controller.crawler import(
    get_user_timeline, get_user_data
)

bp = Blueprint("apis", __name__, url_prefix='/api')

# test api
@bp.route('/test',methods=('GET', 'POST'))
def test():
    return "Api connection test succeeded"

@bp.route('/testenv')
def testenv():
    return current_app.config["MONGODB_URL"]

@bp.route('/buzzer', methods=('GET', 'POST',))
def buzzer():
    screen_name = request.values.get('screenname')
    return make_response({'screenname':screen_name, 'prob':random.random()},401)

@bp.route('/timeline', methods=('GET', 'POST'))
def timeline():
    # get request variable
    screen_name = request.values.get('screenname')
 
    # define what to do at timeline route
    # basicly just run whole tcrawl at timeline but searh first lol
    # return results & status
    db_timeline = get_twitter_timeline()
    # check if particular user already exist in database
    if db_timeline.count_documents({'screen_name': str(screen_name)}, limit=1) < 1:
        get_user_timeline(screen_name) #do crawler to db

    # return existing results
    results = db_timeline.find({'screen_name':str(screen_name)}).limit(5) # select top 5 results
    results = list(results)
    
    return make_response(jsonify(results),401)

# define
@bp.route('/userdata', methods=('GET', 'POST'))
def userdata():
        # get request variable
    screen_name = request.values.get('screenname')
 
    # define what to do at timeline route
    # basicly just run whole tcrawl at timeline but searh first lol
    # return results & status
    #db_user = get_twitter_users() #refer to db
    # check if particular user already exist in database
    #if db_user.count_documents({'screen_name': str(screen_name)}, limit=1) < 1:
    results = get_user_data(screen_name) #do crawler to db
    if results:
        results = results._json
    else:
        results = None
    # return existing results
    #results = db_user.find_one({'screen_name':str(screen_name)}) # select top 5 results
    #results[0].pop('_ids')
    return make_response(jsonify(results),401)
