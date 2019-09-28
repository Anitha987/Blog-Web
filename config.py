import os
class Config :
  '''
  Genarate configuration parent class
  '''
  UPLOADED_PHOTOS_DEST ='app/static/photos'
  SECRET_KEY ="anitha"
  SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://wecode:1234@localhost/pitch'

  #  email configurations
  MAIL_SERVER = 'smtp.googlemail.com'
  MAIL_PORT = 587
  MAIL_USE_TLS = True
  MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
  MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")


class ProdConfig(Config):
  
   SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
class DevConfig(Config):
  '''
  Development  configuration child class

  Args:
      Config: The parent configuration class with General configuration settings
  '''
  DEBUG = True
class TestConfig(Config):
  SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://wecode:1234@localhost/pitch_test'
config_options = {
  'development':DevConfig,
  'production':ProdConfig,
  'test':TestConfig
  }  
 
 
