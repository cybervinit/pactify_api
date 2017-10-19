import os
from flask import Flask
from flask_restplus import Resource, Api
from .models import *

# --------------- Namespace imports ----------------
from .users import users_api
from .pacts import pacts_api
from .seeder import seeds_api
from .conditions import conditions_api

# ---------------------- APP VARIABLE INITIALIZATION -------------

app = Flask(__name__)
api = Api(app)
api.title = 'Pactify API'
api.version = '0.0.1'
# TODO: Add configuration here
app.config.from_object(os.getenv('PACTIFY_API_CONFIG_SETTINGS'))
db.init_app(app)

baseUrl = '/v1/'


# ~~~~~~~~~~~~~~~~~~~~~~~~~~Route setup ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
api.add_namespace(seeds_api, path=baseUrl+'seeds')   # SEEDS
api.add_namespace(users_api, path=baseUrl+'users')   # USERS
api.add_namespace(pacts_api, path=baseUrl+'pacts')   # PACTS
api.add_namespace(conditions_api, path=baseUrl+'conditions')   # CONDITIONS


@api.route(baseUrl+'dbCheck')
class DB_TEST(Resource):
	def get(self): 
		try:
			person = User.query.filter_by(username='cybervinit').first()
			return {'name': person.email}, 222
		except Exception as e:
			return {'server_error': str(e)}, 522

	def post(self):
		try:
			# TODO: post something random
			user1 = User('cybervinit', 'vinit@gmail.com')
			db.session.add(user1)
			db.session.commit()
			return {'message': 'success'}, 222
		except Exception as e:
			return {'server_error': str(e)}, 522





@api.route(baseUrl+'createdb')
class Db_Create(Resource):
	def post(self):
		try:
			db.create_all()  # REACTIVATE by removing comment #
			return {'message': 'REACTIVATE FOR COMMAND'}, 522
		except Exception as e:
			return {'server_error': str(e)}, 522

