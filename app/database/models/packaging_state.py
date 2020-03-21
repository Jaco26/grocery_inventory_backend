from app.database.db import db
from app.database.mixins import BaseMixin, UserDefinedNameMixin

class PackagingState(BaseMixin, UserDefinedNameMixin, db.Model):
  def __init__(self, **kwargs):
    super(PackagingState, self).__init__(**kwargs)