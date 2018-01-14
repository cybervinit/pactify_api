from flask_restplus import Namespace, Resource, fields, reqparse
from .models import db, Pact, Condition

# Self made
from .throw import throw
from .usageModels.session_client import sess

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
one_condition_post_parser.add_argument('session_id', type=str)
one_condition_post_parser.add_argument('value', type=str)
one_condition_post_parser.add_argument('doer', type=str)
one_condition_post_parser.add_argument('issuer', type=str)
one_condition_post_parser.add_argument('issuer', type=str)

@conditions_api.route('/<int:pact_id>')
class SingleCondition(Resource):

	# CAUTION: expects pact_id to exist!
	@conditions_api.expect(one_condition_post_parser)
	def post(self, pact_id):
		args = one_condition_post_parser.parse_args()
		if (not sess.check(args['session_id'])): # Unauthenticated access attempt
			throw("sorry, you don't have access rights to this content", 422)
		c1 = Condition(pact_id, args['value'], args['doer'], args['issuer'], False)
		db.session.add(c1)
		db.session.commit()
		return {'server_error': 'no'}, 222

		# add a new condition



# ----------------------------------------------------------------------------------------

condition_state_parser = reqparse.RequestParser()
condition_state_parser.add_argument('session_id', type=str)
condition_state_parser.add_argument('is_passed', type=bool)

@conditions_api.route('/<string:username>/<int:pact_id>/<int:cond_id>')
class ChangeConditionState(Resource):

	def updatePactState(self, pact_id):
		condList = Condition.query.filter(pact_id=pact_id)
		pact = Pact.query.filter(pact_id=pact_id).first()
		for cond in condList:
			if (cond.status == -1):
				pact.status = -1
				db.session.commit()
				return True
			elif (cond.status == 0):
				return False
		pact.status = 1;
		db.session.commit()

	@conditions_api.expect(condition_state_parser)
	def post(self, username, pact_id, cond_id):
		args = condition_state_parser.parse_args()
		if (not sess.check(args['session_id'])): # Unauthenticated access attempt
			throw("sorry, you don't have access rights to this content", 422)
		
		c1 = Condition.query.filter(pact_id=pact_id, id=cond_id).first()
		c1.is_passed = True # Can only be set to true # args['is_passed'] 
		db.session.commit()
		repull = self.updatePactState(pact_id)
		return {'server_error': 'no', 'repull': repull }, 222


