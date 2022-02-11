from datetime import datetime
from flaskblog import db,Lm
from flask_login import UserMixin 

@Lm.user_loader
def load_user(id):
	return User.query.get(int(id))


class User(db.Model,UserMixin):
	id=db.Column(db.Integer,primary_key=True)
	FirstName=db.Column(db.String(100))
	LastName=db.Column(db.String(100))
	username=db.Column(db.String,unique=True,nullable=False)
	email=db.Column(db.String,unique=True,nullable=0)
	image_file=db.Column(db.String(20),nullable=False,default='default.jpg')
	occupation=db.Column(db.String,nullable=False,default='User')
	bio=db.Column(db.String(100))
	about=db.Column(db.String)
	contact=db.Column(db.Integer)
	fbLink=db.Column(db.String)
	igLink=db.Column(db.String)
	twtLink=db.Column(db.String)
	WaLink=db.Column(db.String)
	location=db.Column(db.String)
	password=db.Column(db.String(100),nullable=False)
	posts=db.relationship('Post',backref='author',lazy="dynamic")


	def __repr__(self):
		return f'User("{self.username}","{self.location}")'

	
		

class Post(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	image_file=db.Column(db.String(20),nullable=True,default='default.jpg')
	title=db.Column(db.String(40))
	content=db.Column(db.Text,nullable=True)
	pub_date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

	def __repr__(self):
		return f'Post("{self.image}","{self.content}","{self.pub_date}")'
