from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, ConfirmForm
from ..import db

@auth.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user= User.query.filter_by(username=form.username.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('Invalid username or password.')
	return render_template('auth/login.html', form=form)
	
@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('main.index'))
	
@auth.route('/register', methods=['GET','POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Your account is activated' )
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', form=form)
	
@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
    	if current_user.verify_password(form.old_password.data):
    		current_user.password= form.password.data
    		db.session.add(current_user)
    		db.session.commit()
    		flash('Your password has been buodated.')
    		return redirect(url_for('main.index'))
    	else:
    		flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)
    
@auth.before_app_request
def before_request():
 	if current_user.is_authenticated:
 		current_user.ping()
 		if not current_user.confirmed and request.endpoint[:5] != 'auth.':
 			return redirect(url_for('auth.unconfirmed'))
 			

@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')
	
@auth.route('/confirmed', methods=['GET', 'POST'])
@login_required
def confirmed():
	form = ConfirmForm()
	if form.validate_on_submit():
		#if current_user.username == form.username.data:
			user= User.query.filter_by(username=form.username.data).first()
			user.confirmed=True
			db.session.add(user)
			db.session.commit()
			flash('This account is confirmed' )
			return redirect(url_for('main.index'))
	return render_template('auth/confirmed.html',form=form)
	
