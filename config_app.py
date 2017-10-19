import os



class BaseConfig(object):
	TESTING = False
	SQLALCHEMY_DATABASE_URI = ''



class DevelopmentConfig(BaseConfig):
	basedir = os.path.abspath(os.path.dirname(__file__))
	SQLALCHEMY_DATABASE_URI = 'postgresql:///' +'pactifydb' #os.environ['DATABASE_URL']
	SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(BaseConfig):
	SQLALCHEMY_DATABASE_URI = 'postgres://txgwqutxuohxjf:e5424382e7ac4249359ba978e4c11958357d91d15f71994d1d1d6706ef24d6d8@ec2-107-20-141-145.compute-1.amazonaws.com:5432/d2vge8h1i37ukv'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	