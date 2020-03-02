from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from app.database.db import db

class BaseMixin:
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

  def save(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()