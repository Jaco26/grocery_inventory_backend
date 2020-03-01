from sqlalchemy.dialects.postgresql import UUID, JSON

from app.database.db import db
from app.database.mixins import BaseMixin

class FoodKind(BaseMixin, db.Model):
  name = db.Column(db.String, nullable=False)
  nutrition_info = db.Column(JSON(none_as_null=True))
  notes = db.Column(db.String)
  
  categories = db.relationship('FoodCategory', secondary='food_kind_category', lazy='subquery',
                              backref=db.backref('food_kinds', lazy=True))
  