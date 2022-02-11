from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager
from flask_migrate import Migrate
from .config import Config




app=Flask(__name__)

db=SQLAlchemy(app)
bc=Bcrypt(app)
Lm=LoginManager(app)
Lm.login_view='login'
migrate = Migrate(app, db)
app.config.from_object(Config)


from flaskblog import routes,models,errors