from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import HTTPException
from app.util import ApiResponse
from app.util.json_validation import create_schema, should_look_like
from app.database.models import AppUser

user_credentials_schema = create_schema({
  'username': str,
  'password': str,
})

account_bp = Blueprint('account_bp', __name__)

@account_bp.route('/register', methods=['POST'])
def register():
  res = ApiResponse()
  try:
    body = should_look_like(user_credentials_schema)
    if AppUser.query.filter_by(username=body['username']).first():
      res.status = 400
      res.msg = 'Username {} already exists in our system'.format(body['username'])
    else:
      AppUser(**body).save()
      res.status = 201
  except HTTPException as exc:
    return exc
  except BaseException as exc:
    res.status = 500
    res.msg = str(exc)
  return res

