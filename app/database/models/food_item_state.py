from sqlalchemy.dialects.postgresql import UUID

from app.database.db import db
from app.database.mixins import TimestampMixin


class FoodItemState(TimestampMixin, db.Model):
  food_item_id = db.Column(UUID(as_uuid=True), db.ForeignKey('food_kind.id'))
  packaging_kind_id = db.Column(UUID(as_uuid=True), db.ForeignKey('packaging_kind.id'))
  packaging_state_id = db.Column(UUID(as_uuid=True), db.ForeignKey('packaging_state.id'))
  number_of_servings = db.Column(db.Integer, default=0)
  weight = db.Column(db.Integer, default=0)
  
  # has lazy loaded 'backref'ed relationship field 'food_item'

  packaging_kind = db.relationship('PackagingKind', lazy='joined')
  packaging_state = db.relationship('PackagingState', lazy='joined')

