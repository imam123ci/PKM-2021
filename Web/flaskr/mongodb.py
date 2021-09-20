# mongodb connector
import click
from flask import current_app, g
from flask.cli import with_appcontext

from pymongo import MongoClient

def get_con():
    error = ""

    if 'mongodb' not in g:
        try:    
            g.mongodb = MongoClient(current_app.config["MONGODB_URL"])
            
        except:
            error = "can't enstablish mongodb connection, please chek your authetication"
        
    if error:
        print (error)
        return None

    return g.mongodb

# get database buzzer
def get_db():
    client = get_con()
    db = client[current_app.config["MONGODB_DB"]]
    return db

def close_db(e=None):
    db = g.pop('mongodb', None)

    if db is not None:
        db.close()
    
    return None

# get document twitter timeline
def get_twitter_timeline():
    db = get_db()
    if db :
        twitter_timeline = db['twitterTimeline'] #specify documents
    else:
        error = "Something Wrong with database"
        return None

    return twitter_timeline

# get document twitter users
def get_twitter_users():
    db = get_db()
    if db :
        twitter_timeline = db['twitterUsers'] #specify documents
    else:
        error = "Something Wrong with database"
        return None

    return twitter_timeline

def test_db():
    r = f"test results: {get_twitter_users()}"
    return r

@click.command('db-test')
@with_appcontext
def init_db_command():
    click.echo(test_db())

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)