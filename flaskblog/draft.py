#the routes below will trigger the followers and followed actions

@app.route('/follow/<username>',methods=['POST','GET'])
@login_required
def follow(username):
	form=EmptyForm()
	if form.validate_on_submit():
		user=User.query.filter_by(username=username).first()
		if user is None:
			flash('User {} not found.'.format(username))
			return redirect(url_for('index'))
		if user == current_user:
			flash('You cannot follow yourself!')
			return redirect(url_for('account',
				username=username)
			)
		current_user.follow(user)
		db.session.commit()
		flash('you are following {}!'.format(username))
		return redirect(url_for('account',
			username=username)
		)
	else:
		return redirect(url_for('index'))

@app.route('/unfollow/<username>',methods=['POST','GET'])
@login_required
def unfollow(username):
	form=EmptyForm()
	if form.validate_on_submit():
		user=User.query.filter_by(username=username).first()
		if user is None:
			flash('User {} not found.'.format(username))
			return redirect(url_for('index'))
		if user == current_user:
			flash('You cannot unfollow yourself!')
			return redirect(url_for('account',
				username=username))
		current_user.unfollow(user)
		db.session.commit()
		flash('you are not following {}!'.format(username))
		return redirect(url_for('account',
			username=username))
	else:
		return redirect(url_for('index'))
