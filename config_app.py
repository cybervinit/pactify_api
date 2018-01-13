import os



class BaseConfig(object):
	TESTING = False
	SQLALCHEMY_DATABASE_URI = ''



class DevelopmentConfig(BaseConfig):
	basedir = os.path.abspath(os.path.dirname(__file__))
	  #os.environ['DATABASE_URL']  # postgresql:///pactifydb
	SQLALCHEMY_DATABASE_URI = "postgresql:///pactifydb"
	SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(BaseConfig):
	SQLALCHEMY_DATABASE_URI = 'postgres://iulhebxzlnybnw:0797e5fef3f9143615b2de8d4e51406b1af6dd15bfbeac988c1210c40cebb25c@ec2-54-235-88-58.compute-1.amazonaws.com:5432/d5n694s9o76kg0'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	