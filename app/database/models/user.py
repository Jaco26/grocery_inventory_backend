from app.database.db import db
from app.database.mixins import TimestampMixin

class AppUser(TimestampMixin, db.Model):
  username = db.Column(db.String, nullable=False, unique=True)
  pw_hash = db.Column(db.String, nullable=False)