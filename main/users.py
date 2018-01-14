from flask_restplus import Namespace, Resource, fields, reqparse
from .models import db, User
import bcrypt
from .usageModels.session_client import sess

from .throw import throw

from .usageModels.arg_parsers import session_only


users_api = Namespace('users', description="User operations")


# ---------------------------------------------------------------------- GET SINGLE USER

user_model = users_api.model('user', {
	'server_error': fields.String(default = "no"),
	'id': fields.Integer,
	'username': fields.String,
	'email': fields.String,
	'longestStreak': fields.Integer,
	'currentStreak': fields.Integer,
	'standard': fields.Integer
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
		person = User.query.filter_by(username=username).first()
		if (not person):
			throw("person doesn't exist", 422)
		return person, 222


# ---------------------------------------------------------------------- SIGNUP USER

@users_api.route('/')
class PostSingleUser(Resource):
	
	def makeUser(self, args):
		checkerUser = User.query.filter_by(username=args['username']).first()
		if (checkerUser):
			throw("username already exists", 422)

		passwordHash = bcrypt.hashpw(args['password'], bcrypt.gensalt(4))
		person = User(args['username'], args['email'], passwordHash) 
		db.session.add(person)
		db.session.commit()

	# SIGNUP -------------------------------
	@users_api.expect(new_user_fields)
	def post(self):
		args = one_user_post_parser.parse_args()
		username = args['username']
		self.makeUser(args)
		sess.add(username, username)
		sessID = sess.get(username)
		return { 'session_id': sessID }, 222


# ---------------------------------------------------------------------- LOGIN USER

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
		try:
			args = one_user_post_parser.parse_args()
			loginSuccess = self.getLoginSuccessful(args)
			loginMessage =  "incorrect username or password"
			if (loginSuccess):
				sess.add(args['username'], args['username'])
				loginMessage = "successfully logged in"
			return {'message': loginMessage}, 200
		except Exception as e:
			raise e
			return {'message': 'error'}, 200

# ----------------------------------------------------------------------- LOGOUT USER

@users_api.route('/logout/<string:username>')
class Logout(Resource):
	
	def get(self, username):
		if (sess.check(username)):
			sess.pop(username)
		else:
			return {'message': 'already logged out'}, 322
		return {'message': 'successful logout'}, 200


# --------------------------------------------------------------------------- CHECK FOR USER LOGIN (TEMP) TODO: DELETE
@users_api.route('/dashboard/<string:username>') 
class Dashboard(Resource):

	def get(self, username):
		if (sess.check(username)):
			return {'message': 'logged in!'}, 200
		else:
			return {'message': 'you have to log in Dx'}, 200











