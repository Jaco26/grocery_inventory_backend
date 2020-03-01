from flask import Response, json

class ApiResponse:
  def __init__(self):
    self.res = Response()
    self.data = None
    self.pvt_msg = ''
    self.pub_msg = ''
    self.status = 200

  @property
  def headers(self):
    return self.res.headers

  @headers.setter
  def headers(self, headers):
    self.res.headers = headers

  def to_flask_response(self):
    self.res.set_data(json.dumps({
      'data': self.data,
      'pvt_msg': self.pvt_msg,
      'pub_msg': self.pub_msg
    }))
    self.res.status_code = self.status
    self.res.mimetype = 'application/json'
    return self.res