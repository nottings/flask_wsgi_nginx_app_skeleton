import os
from flask import send_from_directory, session, render_template, request, redirect
from flask.ext.login import login_user, logout_user, login_required
from . import app, api

login_manager.init_app(app)
login_manager.login_view = '/login'

API_ROOT = '/api'

# Add URI Resources
api.add_resource(RootDoc, API_ROOT)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/', 'favicon.ico')


@app.route('/')
def index():
    """
    """
    return render_template('index.html')

@login_manager.user_loader
def load_user(userid):
    return UserLogin(uid=userid)

