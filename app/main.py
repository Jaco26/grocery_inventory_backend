from flask import request, render_template
from app.extensions import JSONFlask, jwt, db
from app.util import ApiResponse

from app.database.models import *
from app.database.junction_tables import *

def create_app(config=None):
  app = JSONFlask(__name__)
  if config:
    app.config.from_object(config)
  
  db.init_app(app)
  jwt.init_app(app)

  @app.route('/', defaults={'path': ''})
  @app.route('/<path:path>')
  def catch_all(path):
      return app.send_static_file("index.html")

  return app