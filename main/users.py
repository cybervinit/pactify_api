from flask_restplus import Namespace, Resource, fields, reqparse
from .models import db, User


users_api = Namespace('users', description="User operations")



user_model = users_api.model('user', {
	'server_error': fields.String(default = "no"),
	'id': fields.Integer,
	'username': fields.String,
	'email': fields.String,
	})

singleUserParser = reqparse.RequestParser()
singleUserParser.add_argument('username', location='args')

one_user_post_parser = reqparse.RequestParser()
one_user_post_parser.add_argument('username', type=str)
one_user_post_parser.add_argument('email', type=str)

new_user_fields = users_api.model('User', {
	'username': fields.String,
	'email': fields.String
	})

@users_api.route('/<string:username>')
class SingleUser(Resource):

	@users_api.marshal_with(user_model)
	def get(self, username):
		try:
			person = User.query.filter_by(username=username).first()
			return person, 222
		except Exception as e:
			return {'server_error': str(e)}, 522

	@users_api.expect(new_user_fields)
	def post(self):
		try:
			args = one_user_post_parser.parse_args()
			person = User(args['username'], args['email'])
		except Exception as e:
			raise e



