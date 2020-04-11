from app.database.db import db
from app.database.mixins import TimestampMixin

class AppUser(TimestampMixin, db.Model):
  email = db.Column(db.String, nullable=False, unique=True)
  pw_hash = db.Column(db.String, nullable=False)

  @classmethod 
  def get_by_email(cls, email):
    return cls.query.filter(cls.email == email).first()

