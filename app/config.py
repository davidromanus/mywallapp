import os
#from app import app
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "mylittlesecret++--==//()((())"


class DevConfig(Config):
	DEBUG=True
	SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URI') or 'sqlite:///'+os.path.join(basedir,'database.db')
	SQLALCHEMY_TRACK_MODIFICATIONS=False
	ENVIRONMENT='development'	

class ProductionConfig(Config):
	DEBUG=False
	SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URI') or 'sqlite:///'+os.path.join(basedir,'database.db')
	SQLALCHEMY_TRACK_MODIFICATIONS=False
		