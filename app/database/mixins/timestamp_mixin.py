from datetime import datetime
from sqlalchemy.dialects.postgresql import TIMESTAMP
from app.database.db import db
from app.database.mixins import BaseMixin

class TimestampMixin(BaseMixin):
  date_created = db.Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
  date_updated = db.Column(TIMESTAMP(timezone=True), onupdare=datetime.utcnow)
