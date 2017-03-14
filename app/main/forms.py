from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User
from flask_login import login_user, login_required, logout_user, current_user

#Required() validator ensures that the field is not submitted empty	
class NameForm(Form):
	name=StringField('What is your name?', validators=[Required()])
	submit= SubmitField('Submit')
	
class EditProfileForm(Form):
	name = StringField('Real name', validators=[Length(0, 64)])
	location = StringField('Location', validators=[Length(0,64)])
	about_me = TextAreaField('About me')
	submit = SubmitField('Submit')


class EditProfileAdminForm(Form):
	username = StringField('Username',validators=[Required(), Length(1,64)])
	confirmed = BooleanField('Confirmed')
	role = SelectField('Role', coerce=int)
	name = StringField('Real name', validators=[Length(0,64)])
	location = StringField('Location', validators=[Length(0,64)])
	about_me = TextAreaField('About me')
	submit = SubmitField('Submit')
	
	def __init__(self,user,*args, **kwargs):
		super(EditProfileAdminForm, self).__init__(*args,**kwargs)
		self.role.choices = [(role.id,role.name) for role in Role.query.order_by(Role.name).all()]
		self.user=user
	
	
	def validate_username(self,field):
		if field.data != self.user.username and User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use.')

class PostForm(Form):
	body = PageDownField("What's on your mind?", validators=[Required()])
	submit = SubmitField('Submit')
	
class CommentForm(Form):
	body= StringField('Enter your comment',validators=[Required()])
	submit = SubmitField('Submit')
