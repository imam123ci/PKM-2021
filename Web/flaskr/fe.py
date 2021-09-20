# front end blueprint

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('fe', __name__)

@bp.route('/')
def home():
    return render_template('fe/home.html')

@bp.route('/apis')
def api():
    return render_template('fe/apis.html')

@bp.route('/result')
def result():
    return render_template('/fe/result.html')
