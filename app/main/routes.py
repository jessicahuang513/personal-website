from datetime import datetime
from flask import render_template, redirect, url_for, current_app
from app import db
from app.main import bp
from app.models import Post

@bp.route('/')
@bp.route('/index')
def index():
	return render_template('index.html')