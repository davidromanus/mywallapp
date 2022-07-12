from datetime import datetime
from flask import render_template,redirect,url_for,flash,request
from app import app,db,bc#,client
from app.forms import RegistrationForm,LoginForm,EditProfileForm
from app.models import User
from flask_login import login_user,current_user,logout_user,login_required
from werkzeug.urls import url_parse
import os
from app.utils import save_picture,save_post_picture




@app.route('/')
@app.route('/index/')
def index():
	return render_template('index.html')




@app.route('/login',methods=['POST','GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(username=form.username.data).first()
		if user and bc.check_password_hash(user.password,form.password.data):
			login_user(user)
			return redirect(url_for('account',username=current_user.username))
		if user is None or not user.username:
			flash('invalid usernameor password',
				'danger')
		next_page=request.args.get('next')
		if not next_page or url_parse(next_page).netloc !='':
			next_page=url_for('main.index')
		return redirect(next_page)
	return render_template('login.html',
		form=form,
		title='login ')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
    	if form.validate_on_submit():
    		hp=bc.generate_password_hash(form.password.data)
    		if form.picture.data:
    			picture_file=save_picture(form.picture.data)
    		user=User(email=form.email.data,username=form.username.data,password=hp,image_file=picture_file)
    		db.session.add(user)
    		db.session.commit()
    		flash('Your account has been Created')
    		return redirect(url_for('login'))
    return render_template('register.html', form=form)

#account info ans set-up starts here
@app.route('/<username>')
def account(username):
	user=User.query.filter_by(username=username).first()
	if user is None:
		return redirect(url_for('index'))
	picture=url_for('static',filename='profile_pics/' + user.image_file)
	return render_template('account.html',user=user,title='profile',picture=picture)




@app.route('/edit_profile/',methods=['POST','GET'])
@login_required
def edit_profile():
	form=EditProfileForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file=save_picture(form.picture.data)
			current_user.image_file=picture_file
		current_user.username=form.username.data
		current_user.full_name=form.full_name.data
		current_user.about_me=form.about_me.data
		current_user.bio=form.bio.data
		current_user.fb_name=form.fb_name.data
		current_user.ig_name=form.ig_name.data
		current_user.twt=form.twt.data
		current_user.lnk=form.lnk.data
		db.session.commit()
		flash('your  profile has been updated.','success')
		return redirect(url_for('account',
			username=current_user.username,
			about_me=current_user.about_me,
			full_name=current_user.full_name,
			bio=current_user.bio,fb_name=current_user.fb_name,twt=current_user.twt,ig_name=current_user.ig_name,
			lnk=current_user.lnk)
		)
	elif request.method=='GET':
	    form.username.data=current_user.username
	    form.full_name.data=current_user.full_name
	    form.bio.data=current_user.bio
	    form.about_me.data=current_user.about_me
	    form.twt.data=current_user.twt
	    form.ig_name.data=current_user.ig_name
	    form.fb_name.data=current_user.fb_name
	    form.lnk.data=current_user.lnk
	return render_template('edit_profile.html',form=form)


@app.route('/dashboard')
@login_required
def admin_dashboard():
	if current_user.is_authenticated and current_user.roles != True:
		return redirect(url_for('login'))
	users=User.query.order_by(User.date_joined.desc()).all()
	return render_template('admin.html', title="Ugo Dashboard",users=users)
