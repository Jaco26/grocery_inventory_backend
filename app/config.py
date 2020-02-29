import os

class BaseConfig:
  ENABLE_CORS = True
  LOG_LEVEL = os.environ['LOG_LEVEL']

  JWT_BLACKLIST_ENABLED = True
  JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
  JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']

  SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
  SQLALCHEMY_TRACK_MODIFICATIONS = False