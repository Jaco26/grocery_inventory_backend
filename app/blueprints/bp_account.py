import os
import time
from datetime import timedelta
from passlib.hash import pbkdf2_sha256
from flask import Blueprint, request, abort, render_template
from flask_jwt_extended import (
  jwt_required,
  fresh_jwt_required,
  jwt_refresh_token_required,
  create_access_token,
  create_refresh_token,
  get_raw_jwt,
  get_jwt_identity,
)
from werkzeug.exceptions import HTTPException
from app.util import ApiResponse
from app.extensions.mail import mail
from app.util.json_validation import create_schema, should_look_like
from app.database.models import AppUser, RevokedToken, PwResetEmail

user_credentials_schema = create_schema({
  ('email', ''): str,
  ('password', ''): str,
})

send_reset_link_schema = create_schema({
  'email': str
})

pw_reset_schema = create_schema({
  'password': str
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
      pw_hash = pbkdf2_sha256.hash(body['password'])
      AppUser(email=body['email'], pw_hash=pw_hash).save()
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
    if app_user and pbkdf2_sha256.verify(body['password'], app_user.pw_hash):
      res.data = {
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


@account_bp.route('/send-reset-link', methods=['POST'])
def send_reset_link():
  res = ApiResponse()
  try:
    body = should_look_like(send_reset_link_schema)
    app_user = AppUser.get_by_email(body['email'])
    if app_user:
      # delete all records of previously sent pw reset emails so that
      # there will only be one valid link --- mitigate possibility of
      # pw reset link falling into the wrong hands
      for prev_email in PwResetEmail.find_by_user_id(app_user.id):
        prev_email.delete()

      # create new pw_reset_email record
      pw_reset_email = PwResetEmail(user_id=app_user.id)
      pw_reset_email.save()

      fresh_jwt = create_access_token(pw_reset_email.nonce,
                                      fresh=True,
                                      user_claims={ 'email': body['email'] },
                                      expires_delta=timedelta(minutes=30))

      client_host = os.getenv('CLIENT_HOST')
      nonced_link = client_host + '/login/recover/' + fresh_jwt

      mail.send_message(subject='Grocery Inventory Password Reset',
                        recipients=[body['email']],
                        html=render_template('password_reset_email.html', nonced_link=nonced_link))
    res.status = 201
    res.pub_msg = 'If the email address you provided us is in our system you should recieve an email with a link to reset your password.'
  except HTTPException as exc:
    print(exc)
    return exc
  except BaseException as exc:
    print(exc)
    abort(500)
  return res


@account_bp.route('/reset', methods=['POST'])
@fresh_jwt_required
def reset_password():
  res = ApiResponse()
  try:
    body = should_look_like(pw_reset_schema)
    nonce = get_jwt_identity()
    pw_reset_email = PwResetEmail.query.get(nonce)
    if pw_reset_email:
      app_user = AppUser.query.get(pw_reset_email.user_id)
      app_user.pw_hash = pbkdf2_sha256.hash(body['password'])
      app_user.save()
      pw_reset_email.delete()
      res.status = 200
    else:
      res.status = 400
      res.pub_msg = 'This link has expired.'
  except HTTPException as exc:
    print(exc)
    return exc
  except BaseException as exc:
    print(exc)
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
    


