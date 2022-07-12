from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager
from flask_migrate import Migrate
from .config import DevConfig,ProductionConfig


app=Flask(__name__)

db=SQLAlchemy(app)
bc=Bcrypt(app)
Lm=LoginManager(app)
Lm.login_view='login'
migrate = Migrate(app,db)
app.config.from_object(ProductionConfig)



from app import routes,models,errors

if not app.debug:
	import os
	import logging
	from logging.handlers import RotatingFileHandler
	
	if not os.path.exists('logs'):
		os.mkdir('logs')
	file_handler=RotatingFileHandler('logs/ugo.log',maxBytes=10240,backupCount=10)
	file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)

	app.logger.setLevel(logging.INFO)
	app.logger.info('Ugo Startup')
