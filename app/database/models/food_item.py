from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID, DATE

from app.database.db import db
from app.database.mixins import BaseMixin


class FoodItem(BaseMixin, db.Model):
  stock_id = db.Column(UUID(as_uuid=True), db.ForeignKey('stock.id'))
  food_kind_id = db.Column(UUID(as_uuid=True), db.ForeignKey('food_kind.id'))
  date_item_was_new = db.Column(DATE(), default=datetime.utcnow)
  expiration_date = db.Column(DATE(), nullable=False)

  state = db.relationship('FoodItemState', backref='food_item', lazy='joined') # lazy=False/'joined'