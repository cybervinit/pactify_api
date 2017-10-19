from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class BaseModel(db.Model):

	__abstract__ = True

	
	def __repr__(self):
		return '%s(%s)' % (self.__class__.__name__, {
    		column: value
    		for column, value in self._to_dict().items()
    	})
	""" 
    	Can also add a method to JSONify objects
	"""




# pacts_users = db.Table('pacts_users',
# 						db.Column('pact_id', db.Integer, db.ForeignKey('pacts.id'), nullable=False),
# 						db.Column('user_username', db.String(20), db.ForeignKey('users.username'), nullable=False),
# 						db.Column('pact_signed', db.Integer, nullable=False), # -1 if declined, 0 if not seen, 1 if accepted
# 						db.Column('conditions_passed', db.Integer, nullable=False), # -1 if failed, 0 if in progress, 1 if passed
# 						db.PrimaryKeyConstraint('pact_id', 'user_username'))


class Pact_User(BaseModel):
	__tablename__="pacts_users"

	id = db.Column(db.Integer, primary_key=True)

	pact_id = db.Column(db.Integer)
	user_username = db.Column(db.String(20))
	pact_signed = db.Column(db.Integer, nullable=False)
	conditions_passed = db.Column(db.Integer, nullable=False)

	def __init__(self, pact_id, user_username, pact_signed, conditions_passed):
		self.pact_id = pact_id
		self.user_username = user_username
		self.pact_signed = pact_signed
		self.conditions_passed = conditions_passed


# Model class for Users
class User(BaseModel):
	__tablename__="users"

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False, unique=True)
	email = db.Column(db.String(120))


	def __init__(self, username, email):
		self.username = username
		self.email = email


# Model class for Pacts
class Pact(BaseModel):
	__tablename__="pacts"

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(140), nullable=False)
	status = db.Column(db.Integer, nullable=False) # -1 if failed, 0 if in progress, 1 if passed

	def __init__(self, title):
		self.title = title
		self.status = 0


# Model class for Conditions
class Condition(BaseModel):
	__tablename__="conditions"

	id = db.Column(db.Integer, primary_key=True)
	pact_id = db.Column(db.Integer, db.ForeignKey('pacts.id'), nullable=False)
	condition = db.Column(db.String(140), nullable=False)
	doer_username = db.Column(db.String(20), nullable=False)
	issuer_username = db.Column(db.String(20), nullable=False)

	def __init__(self, pact_id, condition, doer_username, issuer_username):
		self.pact_id = pact_id
		self.condition = condition
		self.doer_username = doer_username
		self.issuer_username = issuer_username
		
