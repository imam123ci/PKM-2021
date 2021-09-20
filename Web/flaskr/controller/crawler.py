import tweepy
import click

from flask import current_app, g
from flask.cli import with_appcontext
from flaskr.mongodb import get_twitter_timeline, get_twitter_users #refer to mongodb file

from pymongo import UpdateOne

def get_tcrawl():
    error = None
    if 'tcrawl' not in g:
        if None not in (current_app.config["CONSUMER_KEY"], current_app.config["CONSUMER_SECRET"]):
            auth = tweepy.auth.AppAuthHandler(current_app.config["CONSUMER_KEY"], current_app.config["CONSUMER_SECRET"])
            g.tcrawl = tweepy.API(auth)
        else:
            error= "Please specify twitter consumer key and secret in config.py"
    
    if error:
        print(error)
        return None

    return g.tcrawl

def get_user_timeline(username, textonly=False):
    api = get_tcrawl()
    results = [] #store api results
    resultsdb = []
    error = ""
    try:
        for tweet in tweepy.Cursor(api.user_timeline, screen_name=username, tweet_mode="extended").items(1):
            if textonly:
                results.append(tweet.full_text)

            else:
                try:
                    #make sure value exist or null it
                    t_id = tweet.id
                    t_authorid = tweet.author.id
                    t_created_at = tweet.created_at
                    t_favorite = tweet.favorite_count
                    t_retweet = tweet.retweet_count
                    t_text = tweet.full_text
                    t_source = tweet.source_url

                    # create an array of updateone mongodb
                    # array for bulk insert
                    results.append(tweet)
                    resultsdb.append(UpdateOne(
                        {"_id": str(t_id)},
                        {"$set":{
                                'id' : str(t_id),
                                "author_id" : t_authorid,
                                "screen_name": username,
                                "favorites_count" : t_favorite,
                                "retweets_count" : t_retweet,
                                "source" : t_source,
                                "created_at" : t_created_at,
                                "text" : t_text,
                                }
                            },
                        upsert=True # using upsert to precent duplicate id      
                    ))

                    # get twitter timeline document
                    # refer to mongodb file
                    db_timeline = get_twitter_timeline()  
                    rslt = db_timeline.bulk_write(resultsdb)
                except:
                    # just says somethinf wrong with api
                    # but in truth, it's also mean something wrong with db con
                    error = "Sorry, we can't reach our database"
    except :
        error = "Sorry, we can't reach twitter api right now"

    # log error 
    if error:
        print(error)
        return None #just return none/false if failed

    # for cli results
    if textonly:
        return results

    # return transaction status
    return True

def get_user_data(username, textonly=False):
    api = get_tcrawl()
    error = ""        

    # call twitter api for user data
    try:
        tuser = api.get_user(username)
    except:
        error = "Sorry, we can't reach twitter api right now"
        return None

    #for cli results
    if textonly:
        return tuser

    # for production
    # store data to database
    try:
        db_users =  get_twitter_users()
        db_users.update_one(
            {'_id':str(tuser.id)}, 
            {'$set':{
                'id' : tuser.id,
                'screen_name' : tuser.screen_name,
                'verified' : tuser.verified,
                'protected': tuser.protected,
                'followers_count' : tuser.followers_count,
                'friends_count' : tuser.friends_count,
                'description' : tuser.description,
                'default_profile' : tuser.default_profile,
                'default_profile_image' : tuser.default_profile_image,
                'created_at' : tuser.created_at,
            }}, 
            upsert=True)
    except :
        error = "Sorry, we can't reach twitter api right now"
        return False    
    
    return tuser



@click.command('tcrawl-timeline')
@click.argument('username', required=True)
@click.option('--text', '-t', 'textonly', is_flag=True)
@with_appcontext
def tcraw_cli_timeline(username, textonly):
    click.echo('crawl user timeline')
    r =  get_user_timeline(username, textonly)
    click.echo(r)

@click.command('tcrawl-user')
@click.argument('username', required=True)
@click.option('--text', '-t', 'textonly', is_flag=True)
@with_appcontext
def tcraw_cli_userdata(username, textonly):
    click.echo('crawl user data')
    r =  get_user_data(username, textonly)
    click.echo(r)

def init_app(app):
    app.cli.add_command(tcraw_cli_timeline)
    app.cli.add_command(tcraw_cli_userdata)