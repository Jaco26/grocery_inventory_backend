from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, create_access_token, get_raw_jwt
from werkzeug.exceptions import HTTPException
from app.util import ApiResponse
from app.util.json_validation import create_schema, should_look_like
from app.database.models import AppUser, RevokedToken

user_credentials_schema = create_schema({
  ('username', ''): str,
  ('password', ''): str,
})

account_bp = Blueprint('account_bp', __name__)

@account_bp.route('/register', methods=['POST'])
def register():
  res = ApiResponse()
  try:
    body = should_look_like(user_credentials_schema)
    if AppUser.get_by_username(body['username']):
      res.status = 400
      res.pub_msg = 'Username {} already exists in our system'.format(body['username'])
    else:
      AppUser(username=body['username'], pw_hash=body['password']).save()
      res.status = 201
  except HTTPException as exc:
    return exc
  except BaseException as exc:
    print('EXCEPTION', exc)
    abort(500)
  return res

@account_bp.route('/login', methods=['POST'])
def login():
  res = ApiResponse()
  try:
    body = should_look_like(user_credentials_schema)
    app_user = AppUser.get_by_username(body['username'])
    if app_user:
      res.data = {
        'username': app_user.username,
        'access_token': create_access_token(identity=app_user.id)
      }
      res.status = 200
    else:
      res.status = 401
      res.pub_msg = 'Username or password was not recognized'
  except HTTPException as exc:
    return exc
  except BaseException as exc:
    abort(500)
  return res


@account_bp.route('/logout', methods=['POST'])
@jwt_required
def logout():
  res = ApiResponse()
  try:
    revoked_token = RevokedToken(jti=get_raw_jwt()['jti'])
    revoked_token.save()
  except HTTPException as exc:
    return exc
  except BaseException as exc:
    abort(500)
  return res
    


