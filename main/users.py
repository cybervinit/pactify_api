from flask_restplus import Namespace, Resource, fields, reqparse
from .models import db, User
import bcrypt
from .usageModels.session_client import sess
from .invalid_usage import InvalidUsage

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
one_user_post_parser.add_argument('password', type=str)

new_user_fields = users_api.model('User', {
	'username': fields.String,
	'email': fields.String,
	'password': fields.String
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




@users_api.route('/')
class PostSingleUser(Resource):
	
	def makeUser(self, args):
		passwordHash = bcrypt.hashpw(args['password'], bcrypt.gensalt(4))
		person = User(args['username'], args['email'], passwordHash)
		db.session.add(person)
		db.session.commit()


	@users_api.expect(new_user_fields)
	def post(self):
		try:
			args = one_user_post_parser.parse_args()
			self.makeUser(args)
			sessID = sess.get(username)
			if (sessID):
				return {''}
			return {'message': 'success'}, 222
		except Exception as e:
			# raise e
			return {'server_error': str(e)}, 522


# ----------------------------------------------------------------------

login_fields = users_api.model('Login', {
	'username': fields.String,
	'password': fields.String
	})
login_fields_parser = reqparse.RequestParser()
login_fields_parser.add_argument('username', type=str)
login_fields_parser.add_argument('password', type=str)

@users_api.route('/login')
class Login(Resource):

# Login from here -------- 
	def getLoginSuccessful(self, args):
		username = args['username']
		password = args['password']
		passwordHashFromDb = User.query.filter_by(username=username).first().passwordHash
		return bcrypt.checkpw(password, passwordHashFromDb)

	@users_api.expect(login_fields)
	def post(self):
		# raise InvalidUsage('some error caught')
		try:
			args = one_user_post_parser.parse_args()
			loginSuccess = self.getLoginSuccessful(args)
			if (loginSuccess):
				sess.add(args['username'], args['username'])
			return {'message': str(loginSuccess)}, 200
		except Exception as e:
			raise e
			return {'message': 'error'}, 200
# ----------------------- 

@users_api.route('/logout/<string:username>')
class Logout(Resource):
	
	def get(self, username):
		if (sess.get(username)):
			sess.pop(username)
		else:
			pass
		return {'message': 'successful logout'}, 200


@users_api.route('/dashboard/<string:username>')
class Dashboard(Resource):

	def get(self, username):
		if (sess.get(username)):
			return {'message': 'logged in!'}, 200
		else:
			return {'message': 'you have to log in Dx'}, 200











