from datetime import datetime
from app import db,Lm,app
from flask import current_app
from flask_login import UserMixin,current_user

@Lm.user_loader
def load_user(id):
	return User.query.get(int(id))

ugo_default="""Hello, i am a Ugo User. Ugo makes building a personal brand 
smooth and easy with its beautiful design and
easy to use interface. You can create your Ugo-Page today. It's Free.
"""

class User(db.Model,UserMixin):
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String, unique=True)
	full_name=db.Column(db.String, default="Ugo User")
	email=db.Column(db.String,unique=True)
	password=db.Column(db.String(120))
	date_joined=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	roles=db.Column(db.Boolean,default=False)
	image_file=db.Column(db.String(20),default='file.jpg')
	bio=db.Column(db.String,default='Ugo User')
	about_me=db.Column(db.String,default=ugo_default)
	fb_name=db.Column(db.String)
	ig_name=db.Column(db.String)
	twt=db.Column(db.String)
	lnk=db.Column(db.String)

	def __repr__(self):
		return f'User("{self.username}")'