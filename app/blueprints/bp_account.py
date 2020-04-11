from datetime import timedelta
from flask import Blueprint, request, abort
from flask_jwt_extended import (
  jwt_required,
  jwt_refresh_token_required,
  create_access_token,
  create_refresh_token,
  get_raw_jwt,
  get_jwt_identity,
)
from werkzeug.exceptions import HTTPException
from app.util import ApiResponse
from app.util.json_validation import create_schema, should_look_like
from app.database.models import AppUser, RevokedToken

user_credentials_schema = create_schema({
  ('email', ''): str,
  ('password', ''): str,
})

account_bp = Blueprint('account_bp', __name__)

@account_bp.route('/register', methods=['POST'])
def register():
  res = ApiResponse()
  try:
    body = should_look_like(user_credentials_schema)
    if AppUser.get_by_email(body['email']):
      res.status = 400
      res.pub_msg = 'Email {} already exists in our system'.format(body['email'])
    else:
      AppUser(email=body['email'], pw_hash=body['password']).save()
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
    app_user = AppUser.get_by_email(body['email'])
    if app_user:
      res.data = {
        'email': app_user.email,
        'refresh_token': create_refresh_token(identity=app_user.id, expires_delta=timedelta(days=1)),
        'access_token': create_access_token(identity=app_user.id,
                                            user_claims={ 'email': app_user.email },
                                            expires_delta=timedelta(hours=1)),
      }
      res.status = 200
    else:
      res.status = 401
      res.pub_msg = 'Email or password was not recognized'
  except HTTPException as exc:
    return exc
  except BaseException as exc:
    abort(500)
  return res

@account_bp.route('/refresh-access', methods=['POST'])
@jwt_refresh_token_required
def refresh_access():
  res = ApiResponse()
  try:
    app_user = AppUser.query.get(get_jwt_identity())
    res.data = create_access_token(identity=app_user.id,
                                  user_claims={ 'email': app_user.email },
                                  expires_delta=timedelta(hours=1))
  except HTTPException as exc:
    return exc
  except:
    abort(500)
  return res



@account_bp.route('/logout-access', methods=['POST'])
@jwt_required
def logout_access():
  res = ApiResponse()
  try:
    revoked_token = RevokedToken(jti=get_raw_jwt()['jti'])
    revoked_token.save()
  except HTTPException as exc:
    return exc
  except BaseException as exc:
    abort(500)
  return res


@account_bp.route('/logout-refresh', methods=['POST'])
@jwt_refresh_token_required
def logout_refresh():
  res = ApiResponse()
  try:
    revoked_token = RevokedToken(jti=get_raw_jwt()['jti'])
    revoked_token.save()
  except HTTPException as exc:
    return exc
  except BaseException as exc:
    abort(500)
  return res
    


