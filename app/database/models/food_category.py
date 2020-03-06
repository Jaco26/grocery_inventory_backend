from sqlalchemy.dialects.postgresql import UUID

from app.database.db import db
from app.database.mixins import BaseMixin

class FoodCategory(BaseMixin, db.Model):
  name = db.Column(db.String, nullable=False)
  uniform_name = db.Column(db.String, nullable=False, unique=True)
  # has 'backref'ed field named 'food_kinds'. includes all food_kinds
  # tagged with this food_category