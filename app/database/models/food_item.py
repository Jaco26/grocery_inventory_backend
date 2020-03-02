from datetime import datetime

from sqlalchemy import desc
from sqlalchemy.dialects.postgresql import UUID, DATE

from app.database.db import db
from app.database.mixins import TimestampMixin


class FoodItem(TimestampMixin, db.Model):
  stock_id = db.Column(UUID(as_uuid=True), db.ForeignKey('stock.id'))
  food_kind_id = db.Column(UUID(as_uuid=True), db.ForeignKey('food_kind.id'))
  date_item_was_new = db.Column(DATE(), default=datetime.utcnow)
  expiration_date = db.Column(DATE(), nullable=False)

  # 'states' field in FoodItem instance is sqlalchemy query object which can
  # be used to specify whether or not to grab all previous 'FoodItemState's (a lot)
  # or just the most recent one...or something else
  states = db.relationship('FoodItemState', lazy='dynamic', backref=db.backref('food_item', lazy=True))
  food_kind = db.relationship('FoodKind', lazy='joined')
