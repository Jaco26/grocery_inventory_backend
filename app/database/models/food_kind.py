from sqlalchemy.dialects.postgresql import UUID, JSON

from app.database.db import db
from app.database.mixins import BaseMixin

class FoodKind(BaseMixin, db.Model):
  name = db.Column(db.String, nullable=False)
  category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('food_category.id'))
  nutrition_info = db.Column(JSON(none_as_null=none_as_null=True))
  notes = db.Column(db.String)
  
  