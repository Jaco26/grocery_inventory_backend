from uuid import UUID
from datetime import date, tzinfo, timedelta

from flask import Flask
from flask.json import JSONEncoder

from werkzeug.exceptions import HTTPException, default_exceptions

from app.database.db import db
from app.util import ApiResponse
 


class SimpleUTC(tzinfo):
  def tzname(self, **kwargs):
    return 'UTC'

  def utcoffset(self, dt):
    return timedelta(0)



class CustomJSONEncoder(JSONEncoder):
  def default(self, obj):
    if isinstance(obj, date):
      return obj.replace(tzinfo=SimpleUTC()).isoformat()
    elif isinstance(obj, timedelta):
      return str(obj)
    elif isinstance(obj, UUID):
      return str(obj)
    elif isinstance(obj, db.Model):
      return obj.cols_dict()
    else:
      return JSONEncoder.default(obj)



def create_error_api_response(error):
  res = ApiResponse()
  res.status = error.code if isinstance(error, HTTPException) else 500
  res.pub_msg = str(error)
  res.pvt_msg = str(error)
  return res


class JSONFlask(Flask):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.json_encoder = CustomJSONEncoder

    for code in default_exceptions.keys():
      self.register_error_handler(code, create_error_api_response)


  def make_response(self, rv):
    if isinstance(rv, ApiResponse):
      return rv.to_flask_response()
    return Flask.make_response(self, rv)
