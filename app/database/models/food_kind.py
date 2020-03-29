from sqlalchemy.dialects.postgresql import UUID

from app.database.db import db
from app.database.mixins import BaseMixin, UserDefinedNameMixin


# For things like eggs (I have 3 eggs)
UNIT_OF_MEASURE_IS_SELF_ID = '535207ef-62a7-446e-a7ee-abef66353eb9'

class FoodKind(BaseMixin, UserDefinedNameMixin, db.Model):
  user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('app_user.id'))
  unit_of_measurement_id = db.Column(UUID(as_uuid=True), db.ForeignKey('unit_of_measurement.id'), default=UNIT_OF_MEASURE_IS_SELF_ID)
  serving_size = db.Column(db.Float, default=0.0)

  unit_of_measurement = db.relationship('UnitOfMeasurement', lazy='joined')
  nutrition_info = db.relationship('FoodKindNutritionInfo', lazy='joined', uselist=False)
  categories = db.relationship('FoodCategory', secondary='food_kind_category', lazy='subquery',
                              backref=db.backref('food_kinds', lazy=True))
  stock_items = db.relationship('StockItem', lazy=True)

  def full_dict(self):
    remove = ['unit_of_measurement_id']
    return {
      **{ key: getattr(self, key) for key in self.cols_dict().keys() if key not in remove },
      'unit_of_measurement': self.unit_of_measurement,
      'categories': self.categories,
      'nutrition_info': self.nutrition_info or {}
    }