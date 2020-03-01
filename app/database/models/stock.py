from sqlalchemy.dialects.postgresql import UUID

from app.database.db import db
from app.database.mixins import TimestampMixin


class Stock(TimestampMixin, db.Model):
  user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('app_user.id'))
  name = db.Column(db.String, nullable=False, unique=True)

  snapshots = db.relationship('Snapshot', lazy='dynamic',
                              backref=db.backref('stock', lazy=True))

    