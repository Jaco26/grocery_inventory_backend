import re
from app.database.db import db


def uniform_name(name):
  return re.sub(r'\s+', '_', name.lower())


class UserDefinedNameMixin:
  name = db.Column(db.String, nullable=False)
  uniform_name = db.Column(db.String, nullable=False)

  def __init__(self, **kwargs):
    self.name = kwargs.get('name')
    self.uniform_name = uniform_name(kwargs.get('name'))

  def update_name(self, name):
    self.name = name
    self.uniform_name = uniform_name(name)