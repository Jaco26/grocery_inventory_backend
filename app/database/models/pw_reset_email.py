import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from app.database.db import db

class PwResetEmail(db.Model):
  nonce = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('app_user.id'))

  def save(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  @classmethod
  def find_by_user_id(cls, user_id):
    return cls.query.filter_by(user_id=user_id).all()