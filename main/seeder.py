from flask_restplus import Namespace, Resource, fields, reqparse
from .models import *

seeds_api = Namespace('seeds', description="Seed operations")

user_seeds = [User('vinitsoni', 'vinitsoni357@gmail.com'),
				User('alia', 'alira@gmail.com'),
				User('bobby', 'bobby@gmail.com'),
				User('samuel', 'samuel@gmail.com')]

pact_seeds = [Pact('vinit buys alia icecream'),
				Pact('bobby owes samuel $20'),
				Pact('alia buys vinit lunch')]

condition_seeds = [Condition(1, 'vinit buys alia icecream', 'alia', 'vinitsoni', False),
					Condition(2, 'samuel receives $20 from bobby', 'bobby', 'samuel', False)]


@seeds_api.route('/<string:model>')
class Seed(Resource):

	def post(self, model):
		try:
			return {'message': 'Already Seeded'}, 322
			if (model == 'users'):
				# TODO: seed user's db
				for user in user_seeds:
					db.session.add(user)
				db.session.commit()
				return {'message': 'success'}, 222
			elif (model == 'pacts'):
				for pact in pact_seeds:
					db.session.add(pact)
				db.session.commit()
				for cond in condition_seeds:
					db.session.add(cond)
				db.session.commit()
				return {'message': 'success'}, 222
		except Exception as e:
			raise e