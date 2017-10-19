from flask_restplus import Namespace, Resource, fields, reqparse
from models import db, Pact, Pact_User


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
single_pact_post_fields = pacts_api.model('Title', {'title': fields.String})



@pacts_api.route('/')
class PostSinglePact(Resource):

	@pacts_api.expect(single_pact_post_fields)
	def post(self):
		try:
			args = single_pact_post_parser.parse_args()
			new_pact = Pact(args['title'])
			db.session.add(new_pact)
			db.session.commit()
			return {'message': 'success'}, 222
		except Exception as e:
			return {'server_error': str(e)}, 522

@pacts_api.route('/<int:pact_id>')
class GetSinglePact(Resource):
	
	@pacts_api.marshal_with(pact_model)
	def get(self, pact_id):
		try:
			pact1 = Pact.query.filter_by(id=pact_id).first()
			if (pact1):
				return pact1, 222
			else:
				return {'server_error': 'pact doesn\'t exist'}, 522
		except Exception as e:
			return {'server_error': str(e)}, 522

# -------------------------------- Pact List -------------------------------------

@pacts_api.route('/<string:username>')
class MultiplePact(Resource):

	@pacts_api.marshal_with(pact_list_model)
	def get(self, username):
		try:
			user_pacts = Pact_User.query.with_entities(Pact_User.pact_id).filter_by(user_username=username)
			pact_list = []
			for up in user_pacts:
				pact_list.append(Pact.query.filter_by(id=up.pact_id).first())
			return {'pacts': pact_list}, 222
		except Exception as e:
			return {'server_error': str(e)}, 502

