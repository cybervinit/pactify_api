import os



class BaseConfig(object):
	TESTING = False
	SQLALCHEMY_DATABASE_URI = ''



class DevelopmentConfig(BaseConfig):
	basedir = os.path.abspath(os.path.dirname(__file__))
	SQLALCHEMY_DATABASE_URI = 'postgresql:///' +'pactifydb' #os.environ['DATABASE_URL']
	SQLALCHEMY_TRACK_MODIFICATIONS = False
