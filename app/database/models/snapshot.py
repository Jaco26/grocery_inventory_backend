from sqlalchemy.dialects.postgresql import UUID

from app.database.db import db
from app.database.mixins import TimestampMixin


class AppSnapshot(TimestampMixin, db.Model):
  stock_id = db.Column(UUID(as_uuid=True), db.ForeignKey('app_stock.id'))
  