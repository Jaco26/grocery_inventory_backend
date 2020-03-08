from sqlalchemy.dialects.postgresql import UUID

from app.database.db import db
from app.database.mixins import TimestampMixin

class FoodKindNutritionInfo(TimestampMixin, db.Model):
  food_kind_id = db.Column(UUID(as_uuid=True), db.ForeignKey('food_kind.id'), primary_key=True)
  calories_per_serving = db.Column(db.Integer, default=0)
  notes = db.Column(db.String)