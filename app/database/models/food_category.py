from sqlalchemy.dialects.postgresql import UUID

from app.database.db import db
from app.database.mixins import BaseMixin, UserDefinedNameMixin

class FoodCategory(BaseMixin, UserDefinedNameMixin, db.Model):
  # has 'backref'ed field named 'food_kinds'. includes all food_kinds
  # tagged with this food_category
  def __init__(self, **kwargs):
    super(FoodCategory, self).__init__(**kwargs)
