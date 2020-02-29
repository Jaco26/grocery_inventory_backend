from flask import Flask, render_template

def create_app(config=None):
  app = Flask(__name__)
  if config:
    app.config.from_object(config)
  
  @app.route('/')
  def index():
    return 'Hello, You!'

  return app