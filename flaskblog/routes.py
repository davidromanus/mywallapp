from datetime import datetime
from flask import render_template,redirect,url_for,flash,request
from flaskblog import app,db,bc
from flaskblog.forms import RegistrationForm,LoginForm,PostForm,EditProfileForm,EditPostForm
from flaskblog.models import User,Post
from flask_login import login_user,current_user,logout_user,login_required
from werkzeug.urls import url_parse
import os
from flaskblog.utils import save_picture,save_post_picture



#----------authentication starts here
@app.route('/sign_up',methods=['POST','GET'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form=RegistrationForm()
	if form.validate_on_submit():
		hp=bc.generate_password_hash(form.password.data).decode('utf-8')
		user=User(username=form.username.data,
			email=form.email.data,FirstName=form.FirstName.data,
			LastName=form.LastName.data,
			password=hp,occupation=form.occupation.data,
			contact=form.phoneNumber.data)
		db.session.add(user)
		db.session.commit()
		flash(f'your account has been created','success')
		return redirect('login')
	return render_template('register.html',form=form,title='sign in')


@app.route('/login',methods=['POST','GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('account',username=current_user.username))
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(username=form.username.data).first()
		if user and bc.check_password_hash(user.password,form.password.data):
			login_user(user)
			return redirect(url_for('account',username=user.username))
		if user is None or not user.username:
			flash('invalid usernameor password',
				'danger')
		next_page=request.args.get('next')
		if not next_page or url_parse(next_page).netloc !='':
			next_page=url_for('index')
		return redirect(next_page)
	return render_template('login.html',
		form=form,
		title='login ')

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))
#----------authentication stops here

@app.route('/account/<username>')
def account(username):
	user=User.query.filter_by(username=username).first()
	post=Post.query.filter_by(user_id=user.id).order_by(Post.pub_date.desc()).all()
	image_file=url_for('static',filename='profile_pics/' + user.image_file)
	return render_template('account.html',
		user=user,
		post=post,
		title='profile',
		image_file=image_file)




@app.route('/')
@app.route('/index/')
def index():
	return render_template('index.html')




@app.route('/make_post',methods=['POST','GET'])
@login_required
def make_post():
	form=PostForm()
	if form.validate_on_submit():
		pro_pic=save_post_picture(form.picture.data)
		post=Post(
			content=form.post.data,
			title=form.title.data,
			image_file=pro_pic,
			author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('posted','success')
		return redirect(url_for('account',username=current_user.username))
	return render_template('create_post.html',form=form)



#editing sections:all editings will be handled here

@app.route('/edit_profile/',methods=['POST','GET'])
@login_required
def edit_profile():
	form=EditProfileForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file=save_picture(form.picture.data)
			current_user.image_file=picture_file
		current_user.username=form.username.data
		current_user.FirstName=form.FirstName.data
		current_user.LastName=form.LastName.data
		current_user.email=form.email.data
		current_user.occupation=form.occupation.data
		current_user.contact=form.phoneNumber.data
		current_user.bio=form.bio.data
		current_user.fbLink=form.fbLink.data
		current_user.igLink=form.igLink.data
		current_user.twtLink=form.twtLink.data
		current_user.WaLink=form.WaLink.data
		current_user.location=form.location.data
		current_user.about=form.about.data
		db.session.commit()
		flash('your  profile has been updated.','success')
		return redirect(url_for('account',
			username=current_user.username,
			about=current_user.about,
			FirstName=current_user.FirstName,
			LastName=current_user.LastName,
			email=current_user.email,
			bio=current_user.bio,
			location=current_user.location,
			occupation=current_user.occupation,
			contact=current_user.contact,
			fbLink=current_user.fbLink,
			igLink=current_user.igLink,
			WaLink=current_user.WaLink,
			twtLink=current_user.twtLink)
		)
	elif request.method=='GET':
	    form.username.data=current_user.username
	    form.FirstName.data=current_user.FirstName
	    form.LastName.data=current_user.LastName
	    form.bio.data=current_user.bio
	    form.email.data=current_user.email
	    form.phoneNumber.data=current_user.contact
	    form.location.data=current_user.location
	    form.occupation.data=current_user.occupation
	    form.fbLink.data=current_user.fbLink
	    form.igLink.data=current_user.igLink
	    form.twtLink.data=current_user.twtLink
	    form.WaLink.data=current_user.WaLink
	    form.about.data=current_user.about
	return render_template('edit_profile.html',form=form)



@app.route('/edit_post/<int:id>',methods=['POST','GET'])
@login_required
def edit_post(id):
	form=EditPostForm()
	task_to_edit=Post.query.get_or_404(id)

	if request.method=='POST':
		if form.picture.data:
			picture_file=save_post_picture(form.picture.data)
			task_to_edit.image_file=picture_file
		task_to_edit.content=form.post.data
		task_to_edit.title=form.title.data
		db.session.commit()
		flash('updated successfully','success')
		return redirect(url_for('account',
			username=current_user.username,
			image_file=task_to_edit.image_file,
			title=task_to_edit.title,
			content=task_to_edit.content))
	elif request.method=='GET':
		form.picture.data=task_to_edit.image_file
		form.post.data=task_to_edit.content
		form.title.data=task_to_edit.title
	return render_template('edit-post.html',form=form)


@app.route('/delete/<int:id>')
@login_required
def delete(id):
	item_to_delete=Post.query.get_or_404(id)
	db.session.delete(item_to_delete)
	db.session.commit()
	flash('deleted','danger')
	return redirect(url_for('account'))
#editing ends here