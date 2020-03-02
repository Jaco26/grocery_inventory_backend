from flask import request, render_template
from app.extensions import JSONFlask, jwt, db
from app.util import ApiResponse

from app.database.models import *
from app.database.junction_tables import *

from app.blueprints import (
  account_bp,
  categories_bp,
  food_item_state_bp,
  stock_bp,
  snapshot_bp,
)

def create_app(config=None):
  app = JSONFlask(__name__)
  if config:
    app.config.from_object(config)
  
  db.init_app(app)
  jwt.init_app(app)

  app.register_blueprint(account_bp, url_prefix='/api/v1/account')
  app.register_blueprint(categories_bp, url_prefix='/api/v1/categories')
  app.register_blueprint(food_item_state_bp, url_prefix='/api/v1/food_item_state')
  app.register_blueprint(stock_bp, url_prefix='/api/v1/stock')
  app.register_blueprint(snapshot_bp, url_prefix='/api/v1/snapshot')

  @app.route('/', defaults={'path': ''})
  @app.route('/<path:path>')
  def catch_all(path):
      return app.send_static_file("index.html")

  return app