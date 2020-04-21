import os

class BaseConfig:
  ENABLE_CORS = True
  LOG_LEVEL = os.environ['LOG_LEVEL']

  JWT_BLACKLIST_ENABLED = True
  JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
  JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']

  SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  MAIL_SERVER = 'smtp.gmail.com'
  MAIL_PORT = 465
  MAIL_USE_TLS = False
  MAIL_USE_SSL = True
  MAIL_USERNAME = os.environ['EMAIL_USER']
  MAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
  MAIL_DEFAULT_SENDER = os.environ['EMAIL_USER']