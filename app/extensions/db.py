

def init_app(app):
  from flask_migrate import Migrate
  from app.database.db import db
  from app.database.seeder import seed_db
  
  app.cli.add_command(seed_db)
  db.init_app(app)
  Migrate(app, db)