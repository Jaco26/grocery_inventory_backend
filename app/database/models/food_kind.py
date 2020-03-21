from sqlalchemy.dialects.postgresql import UUID

from app.database.db import db
from app.database.mixins import BaseMixin, UserDefinedNameMixin

class FoodKind(BaseMixin, UserDefinedNameMixin, db.Model):
  unit_of_measurement_id = db.Column(UUID(as_uuid=True), nullable=False)
  units_to_serving_size = db.Column(db.Integer, default=0)

  unit_of_measurement = db.relationship('UnitOfMeasurement', lazy='joined')
  nutrition_info = db.relationship('FoodKindNutritionInfo', lazy='joined', uselist=False)
  categories = db.relationship('FoodCategory', secondary='food_kind_category', lazy='subquery',
                              backref=db.backref('food_kinds', lazy=True))
  

  def full_dict(self):
    return {
      **self.cols_dict(),
      'categories': self.categories,
      'nutrition_info': self.nutrition_info
    }