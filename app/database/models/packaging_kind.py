from app.database.db import db
from app.database.mixins import BaseMixin, UserDefinedNameMixin

class PackagingKind(BaseMixin, UserDefinedNameMixin, db.Model):
  def __init__(self, **kwargs):
    super(PackagingKind, self).__init__(**kwargs)
