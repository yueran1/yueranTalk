from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_script import Shell, Manager
from flask_migrate import Migrate, MigrateCommand
import os

basedir = os.path.abspath(os.path.dirname(__file__))




app = Flask(__name__)





#==================Chapter 5 database====================

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True


#db object instantiated from class SQLAlchemy represents the database
#provides all functionality of FLask-SQLAlchemy
db=SQLAlchemy(app)

#Migrate can implement the database qian yi, to make update databse avoid delete the 
#original database
migrate=Migrate(app,db)
manager=Manager(app)
manager.add_command('db', MigrateCommand)




class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	
	
	#backref add a back reference in the other model in the relationship
	#'User' represents the object-oriented view of the relationship
	users= db.relationship('User', backref='role',lazy='dynamic')
	
	def __repr__(self):
		return '<Role %r>' % self.name
		
class User(db.Model):
	__tablename__='users'
	id = db.Column(db.Integer, primary_key=True)
	username= db.Column(db.String(64), unique=True, index=True)
	role_id= db.Column(db.Integer, db.ForeignKey('roles.id'))

	def __repr__(self):
		return '<User %r>' % self.username


#====================end of chapter 5======================

#The app.config dictionary is a general_purpose place to store configuration variables
#used bt the freamework,entextion,or application itself

#SECRET_KEY is used as encrypyion key by Flask
app.config['SECRET_KEY']= 'hard to guess string'
boostrap= Bootstrap(app)

#direct the page with the path end with '/' to hello world
#Tell flask to resigter the view function as a handler for GET and POST request
#in the URl map. When method is not giver, GET is default
@app.route('/', methods=['GET', 'POST'])
def index():
    #return '<h1>hello World!</h1>'
    name= None
    form= NameForm()
    #When user navigate the app for 1st time, there is no name
    #After user submits a name, this name can be displayed on website
    if form.validate_on_submit():
    	user = User.query.filter_by(username=form.name.data).first()
    	if user is None:
    	
			user= User(username= form.name.data)
			db.session.add(user)
			session['known']= False
    	else:
    		session['known']= True
    	
    	
    	'''old_name= session.get('name')
    	if old_name is not None and old_name != form.name.data:
    		flash("Gai Lai! name is different!")'''
    	
    	
    	#name= form.name.data
    	session['name']= form.name.data
    	
    	form.name.data= ''
    	#The only vaiable in url_for is enpoint, by default, endpoint's name is view 			#function's name
    	return redirect(url_for('index'))
    #Use GET instead of POST to avoid repeatly submit request
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False))

#Direct the page with the path end with /user/<name> to hello user_name
@app.route('/user/<name>')
def user(name):
    #return '<h1>Hello, %s!</h1>' %name
    return render_template('user2.html',name=name)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'),500

#Required() validator ensures that the field is not submitted empty	
class NameForm(FlaskForm):
	name=StringField('What is your name?', validators=[Required()])
	submit= SubmitField('Submit')
	
def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))

#The server startup is routed through manager.run() instead of app.run(), where the command line
#is parsed
if __name__ == '__main__':
    manager.run()

