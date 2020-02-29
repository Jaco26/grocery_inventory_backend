from app.extensions import JSONFlask, jwt, db
from app.util import ApiResponse

def create_app(config=None):
  app = JSONFlask(__name__)
  if config:
    app.config.from_object(config)
  
  db.init_app(app)
  jwt.init_app(app)

  @app.route('/')
  def index():
    res = ApiResponse()
    res.data = 'Hello, You!'
    return res

  return app