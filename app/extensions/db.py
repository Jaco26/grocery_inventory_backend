

def init_app(app):
  from flask_migrate import Migrate
  from app.database.db import db
  
  db.init_app(app)
  Migrate(app, db)