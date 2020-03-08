from sqlalchemy.dialects.postgresql import UUID, JSON

from app.database.db import db
from app.database.mixins import BaseMixin

class FoodKind(BaseMixin, db.Model):
  name = db.Column(db.String, nullable=False)
  uniform_name = db.Column(db.String, nullable=False, unique=True)

  nutrition_info = db.relationship('FoodKindNutritionInfo', lazy='joined', uselist=False)
  categories = db.relationship('FoodCategory', secondary='food_kind_category', lazy='subquery',
                              backref=db.backref('food_kinds', lazy=True))
  
  def full_dict(self):
    return {
      **self.cols_dict(),
      'categories': self.categories,
      'nutrition_info': self.nutrition_info
    }