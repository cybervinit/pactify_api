from flask_restplus import Namespace, Resource, fields, reqparse
from models import db, Pact, Condition

conditions_api = Namespace('conditions', description='Condition operations')

condition_model = conditions_api.model('condition', {
	'pact_id': fields.Integer,
	'doer_username': fields.String(),
	'issuer_username': fields.String()
	})

condition_list_model = conditions_api.model('conditions', {
	'server_error': fields.String(default='no'),
	'conditions': fields.List(fields.Nested(condition_model))
	})

@conditions_api.route('/<int:pact_id>')
class Condition(Resource):

	@conditions_api.marshal_with(condition_list_model)
	def get(self):
		try:
			condition_list = Condition.query.filter_by(pact_id=pact_id)
			return {'conditions': condition_list}, 222
		except Exception as e:
			raise e
			return {'server_error': str(e)}, 522


# ----------------------------------------------------------------------------------------

one_condition_post_parser = reqparse.RequestParser()


one_condition_post_parser.add_argument('value', type=str)
one_condition_post_parser.add_argument('doer', type=str)
one_condition_post_parser.add_argument('issuer', type=str)

@conditions_api.route('/<int:pact_id>')
class SingleCondition(Resource):

	# CAUTION: expects pact_id to exist!
	@conditions_api.expect(one_condition_post_parser)
	def post(self, pact_id):
		try:
			args = one_condition_post_parser.parse_args()
			c1 = Condition(pact_id, args['value'], args['doer'], args['issuer'])
			db.session.add(c1);
			# add a new condition
		except Exception as e:
			raise e
