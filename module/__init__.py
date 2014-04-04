from gevent.monkey import patch_all
patch_all()

from flask import Flask
from flask.ext.restful import Api
from flask.ext.script import Manager

app = Flask(__name__)
app.secret_key = 'some randome string'
api = Api(app)

# Initialize App manager
manager = Manager(app)

import module.models
import module.views
