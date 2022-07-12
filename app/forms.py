from flask_wtf import FlaskForm 
from app import app
from wtforms import IntegerField,TextAreaField,StringField,PasswordField,SubmitField,BooleanField,SelectField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flask_wtf.file import FileField,FileAllowed
from app.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
	username=StringField('Username', validators=[DataRequired()])
	email=StringField('Email',validators=[DataRequired()])
	picture=FileField('Picture',validators=[FileAllowed(['jpg','png','jpeg','jfif','gif']),DataRequired()])
	password=PasswordField('password',validators=[DataRequired(),Length(min=8,max=80)])
	#confirm_password=PasswordField('confirm password',validators=[DataRequired(),EqualTo('password')])
	submit=SubmitField('Join In')


	def validate_email(self,email):
		user=User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('this email address is unavailable')

	def validate_username(self,username):
		user=User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('this username is unavailable!')


class LoginForm(FlaskForm):
	username=StringField('Username',validators=[DataRequired()])
	password=PasswordField('Password',validators=[DataRequired(),Length(min=8,max=80)])
	remember=BooleanField('Rememeber Me')
	submit=SubmitField('submit')



class EditProfileForm(FlaskForm):
	picture=FileField('Picture',validators=[FileAllowed(['jpg','png','jpeg','jfif','gif'])])
	full_name=StringField('Full Name')
	username=StringField('Username')
	about_me=TextAreaField('Edit About Me Info')
	bio=StringField('Edit Job Info')
	fb_name=StringField('Facebook Username')
	ig_name=StringField('Instagram Username')
	lnk=StringField('LinkedIn Username')
	twt=StringField('Twitter Username')
	submit=SubmitField('submit')

	def validate_username(self,username):
		if username.data != current_user.username:
			user=User.query.filter_by(username=username.data).first()
			if user is not None and user == "admin":
				raise ValidationError('this username is unavailable!')
		