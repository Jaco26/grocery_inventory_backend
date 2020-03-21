import re
from app.database.db import db


def uniform_name(name):
  return re.sub(r'\s+', '_', name.lower())


class UserDefinedNameMixin:
  name = db.Column(db.String, nullable=False)
  uniform_name = db.Column(db.String, nullable=False, unique=True)

  def __init__(self, *args, **kwargs):
    self.name = kwargs.get('name')
    self.uniform_name = uniform_name(kwargs.get('name'))