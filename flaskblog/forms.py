from flask_wtf import FlaskForm 
from wtforms import IntegerField,TextAreaField,StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flask_wtf.file import FileField,FileAllowed
from flaskblog.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
	FirstName=StringField('First Name',validators=[DataRequired(),Length(min=2,max=60)])
	LastName=StringField('Last Name',validators=[DataRequired(),Length(min=2,max=60)])
	username=StringField('Username',validators=[DataRequired(),Length(min=2,max=60)])
	email=StringField('Email',validators=[DataRequired()])
	phoneNumber=IntegerField('Phone Number',validators=[DataRequired()])
	occupation=StringField('Occupation',validators=[DataRequired(),Length(min=2,max=40)])
	password=PasswordField('password',validators=[DataRequired(),Length(min=8,max=80)])
	confirm_password=PasswordField('confirm password',validators=[DataRequired(),EqualTo('password')])
	#picture=FileField('Update Profile picture',validators=[FileAllowed(['jpg','png']),DataRequired()])
	submit=SubmitField('submit')

	def validate_username(self,username):
		user=User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('please user a different username')


class LoginForm(FlaskForm):
	username=StringField('username',validators=[DataRequired()])
	password=PasswordField('password',validators=[DataRequired(),Length(min=8,max=80)])
	remember=BooleanField('Rememeber Me')
	submit=SubmitField('submit')



class EditProfileForm(FlaskForm):
	FirstName=StringField('First Name',validators=[DataRequired(),Length(min=2,max=60)])
	LastName=StringField('Last Name',validators=[DataRequired(),Length(min=2,max=60)])
	username=StringField('Username',validators=[DataRequired()])
	email=StringField('Email',validators=[DataRequired()])
	bio=StringField('Bio',validators=[DataRequired()])
	fbLink=StringField('Facebook Link')
	twtLink=StringField('Twitter Link')
	igLink=StringField('Instagram Link')
	WaLink=StringField('WhatsApp Link')
	location=StringField('location',validators=[DataRequired()])
	phoneNumber=IntegerField('Phone Number',validators=[DataRequired()])
	occupation=StringField('Occupation',validators=[DataRequired(),Length(min=2,max=40)])
	about=TextAreaField('about',validators=[DataRequired(),Length(min=100,max=1000)])
	picture=FileField('Update Profile picture',validators=[FileAllowed(['jpg','png'])])
	submit=SubmitField('submit')

	def validate_username(self,username):
		if username.data != current_user.username:
			user=User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('please user a different username')


class PostForm(FlaskForm):
	picture=FileField('Add Prodcut Image',validators=[DataRequired(),FileAllowed(['jpg','png','jpeg','jfif'])])
	title=StringField('Title',validators=[DataRequired()])
	post=TextAreaField('Description',validators=[Length(min=50,max=500)])
	submit=SubmitField('Done')



class EditPostForm(FlaskForm):
	picture=FileField('Add Prodcut Image',validators=[FileAllowed(['jpg','png','jpeg','jfif'])])
	title=StringField('Title',validators=[DataRequired()])
	post=TextAreaField('Description',validators=[Length(min=50,max=500)])
	submit=SubmitField('Update Post')