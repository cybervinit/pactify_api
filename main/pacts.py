from flask_restplus import Namespace, Resource, fields, reqparse
from .models import db, Pact, Pact_User
from .throw import throw
from .usageModels.session_client import sess
from .usageModels.arg_parsers import session_only

pacts_api = Namespace('pacts', description="Pact operations")



pact_model = pacts_api.model('pact', {
	'server_error': fields.String(default="no"),
	'id': fields.Integer,
	'title': fields.String,
	'status': fields.Integer
	})

pact_list_model = pacts_api.model('pact_list', {
	'server_error': fields.String(default="no"),
	'pacts': fields.List(fields.Nested(pact_model))
	})

# ----------------------- SINGLE Pact -----------------------------------------

single_pact_post_parser = reqparse.RequestParser()
single_pact_post_parser.add_argument('title', type=str)
single_pact_post_parser.add_argument('isPublic', type=bool)
single_pact_post_parser.add_argument('session_id', type=str)
single_pact_post_parser.add_argument('party1', type=str)
single_pact_post_parser.add_argument('party2', type=str)

single_pact_post_fields = pacts_api.model('Title', {
	'title': fields.String,
	'party1': fields.String,
	'party2': fields.String,
	'isPublic': fields.Boolean,
	'session_id': fields.String
	})

# ------------------ MAKE NEW PACT -----------------------
@pacts_api.route('/')
class PostSinglePact(Resource):

	def addPact(self, args):
		new_pact = Pact(args['title'], args['isPublic'])
		db.session.add(new_pact)
		db.session.commit()
		pu1 = Pact_User(new_pact.id, args['party1'])
		pu2 = Pact_User(new_pact.id, args['party2'])
		db.session.add(pu1)
		db.session.add(pu2)
		db.session.commit()
		return new_pact


	@pacts_api.expect(single_pact_post_fields)
	@pacts_api.marshal_with(pact_model)
	def post(self):
		args = single_pact_post_parser.parse_args()
		if (not sess.check(args['session_id'])):
			throw('sorry, you don\'t have access rights for this action', 422)
		new_pact = self.addPact(args)
		return new_pact, 222 
	# return to (post the conditions && sign pact by user1 automatically) according to the pact id

# ------------------- SIGN PACT ------------------------------

@pacts_api.route('/sign/<int:pact_id>/<string:username>')
class SignPact(Resource):
	def get(self, pact_id, username):
		args = session_only.parse_args()
		if (not sess.check(args['session_id'])):
			throw('you are not authorized to sign.', 422)
		pact = Pact_User.query.filter(Pact_User.user_username==username, Pact_User.pact_id==pact_id).first()
		pact.pact_signed = True
		db.session.commit()
		return {'message': 'pact signed successfully!'}, 222
		


# ------------------ GET PACT -----------------------

@pacts_api.route('/<int:pact_id>')
class GetSinglePact(Resource):

	@pacts_api.marshal_with(pact_model)
	def get(self, pact_id):
		try:
			args = session_only.parse_args()
			if (not sess.check(args['session_id'])):
				throw('sorry, you dont\' have access rights for this content', 422)
			pact1 = Pact.query.filter_by(id=pact_id).first()
			if (pact1):
				return pact1, 222
			else:
				return {'server_error': 'pact doesn\'t exist'}, 522
		except Exception as e:
			throw(str(e), 522)

# -------------------------------- Pact List -------------------------------------



@pacts_api.route('/<string:username>')
class MultiplePact(Resource):

	@pacts_api.marshal_with(pact_list_model)
	def get(self, username):
		# args = session_only.parse_args()
		
		if (not sess.check(username)): # TODO: change to 'session_id' check!
			throw('sorry, you dont\' have access rights for this content', 402)
		user_pacts = Pact_User.query.filter_by(user_username=username)
		pact_list = []
		for up in user_pacts:
			pact_list.append(Pact.query.filter_by(id=up.pact_id).first())
		return {'pacts': pact_list}, 222
		# except Exception as e:
		# 	throw(str(e), 502)


