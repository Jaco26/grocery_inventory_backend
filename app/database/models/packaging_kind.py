from sqlalchemy.dialects.postgresql import UUID

from app.database.db import db
from app.database.mixins import BaseMixin

class PackagingKind(BaseMixin, db.Model):
  name = db.Column(db.String, nullable=False)
  