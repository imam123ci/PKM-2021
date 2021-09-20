
import click

from flask import current_app, g
from flask.cli import with_appcontext

def classify_tweet(tweet):
    results = "result"
    #results = model.predict(["lol"])
    return results


@click.command('tclassify')
@click.argument('tweet', required=True)
@with_appcontext
def tclassify(tweet):
    click.echo(classify_tweet(str(tweet)))
    
def init_app(app):
    app.cli.add_command(tclassify)