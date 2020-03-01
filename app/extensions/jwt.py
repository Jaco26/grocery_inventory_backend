def init_app(app):
  import functools
  from flask_jwt_extended import JWTManager
  from app.database.models import RevokedToken

  jwt = JWTManager()

  jwt.init_app(app)

  @jwt.token_in_blacklist_loader
  def is_token_revoked(decrypted_token):
    jti = decrypted_token.get('jti')
    return bool(RevokedToken.query.get(jti))