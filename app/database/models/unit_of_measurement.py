from app.database.db import db
from app.database.mixins import BaseMixin, UserDefinedNameMixin

class UnitOfMeasurement(BaseMixin, UserDefinedNameMixin, db.Model):
  def __init__(self, *args, **kwargs):
    # Maybe have to do it like this
    # https://stackoverflow.com/questions/20460339/flask-sqlalchemy-constructor#20462185
    super().__init__(self, *args, **kwargs)