from app.database.db import db
from app.database.mixins import BaseMixin, UserDefinedNameMixin

class UnitOfMeasurement(BaseMixin, UserDefinedNameMixin, db.Model):
  def __init__(self, **kwargs):
    super(UnitOfMeasurement, self).__init__(**kwargs)