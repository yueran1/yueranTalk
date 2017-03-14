import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	#ADMIN = os.environ.get('ADMIN')
	ADMIN = 'admin'
	FLASKY_POSTS_PER_PAGE =20
	FLASKY_FOLLOWERS_PER_PAGE= 50
	FLASKY_COMMENTS_PER_PAGE=20
	
	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
	

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URO = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
	
config ={
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	#'production': ProductionConfig,
	'default': DevelopmentConfig
}