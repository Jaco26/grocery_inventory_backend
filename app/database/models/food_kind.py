from sqlalchemy.dialects.postgresql import UUID

from app.database.db import db
from app.database.mixins import BaseMixin, UserDefinedNameMixin


# For things like eggs (I have 3 eggs)
UNIT_OF_MEASURE_IS_SELF_ID = '0b5c009b-fb3f-4642-a177-71c31f557d27'

class FoodKind(BaseMixin, UserDefinedNameMixin, db.Model):
  user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('app_user.id'))
  unit_of_measurement_id = db.Column(UUID(as_uuid=True), db.ForeignKey('unit_of_measurement.id'), default=UNIT_OF_MEASURE_IS_SELF_ID)
  units_to_serving_size = db.Column(db.Integer, default=0)

  unit_of_measurement = db.relationship('UnitOfMeasurement', lazy='joined')
  nutrition_info = db.relationship('FoodKindNutritionInfo', lazy='joined', uselist=False)
  categories = db.relationship('FoodCategory', secondary='food_kind_category', lazy='subquery',
                              backref=db.backref('food_kinds', lazy=True))
  food_items = db.relationship('FoodItem', lazy=True)

  def full_dict(self):
    return {
      **self.cols_dict(),
      'unit_of_measurement': self.unit_of_measurement.name,
      'categories': self.categories,
      'nutrition_info': self.nutrition_info
    }