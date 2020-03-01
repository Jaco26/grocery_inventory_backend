from sqlalchemy.dialects.postgresql import UUID
from app.database.db import db

class RevokedToken(db.Model):
  jti = db.Column(UUID(as_uuid=True), primary_key=True)

  def save(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()