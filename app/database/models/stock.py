from sqlalchemy.dialects.postgresql import UUID

from app.database.db import db
from app.database.mixins import TimestampMixin


class AppStock(TimestampMixin, db.Model):
  user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('app_user.id'))
  current_snapshot_id = db.Column(UUID(as_uuid=True), db.ForeignKey('app_snapshot.id'))