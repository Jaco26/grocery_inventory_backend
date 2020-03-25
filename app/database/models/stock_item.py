from datetime import datetime

from sqlalchemy import desc, text
from sqlalchemy.dialects.postgresql import UUID, DATE

from app.database.db import db
from app.database.mixins import TimestampMixin


class StockItem(TimestampMixin, db.Model):
  stock_id = db.Column(UUID(as_uuid=True), db.ForeignKey('stock.id'))
  food_kind_id = db.Column(UUID(as_uuid=True), db.ForeignKey('food_kind.id'))
  date_item_was_new = db.Column(DATE(), default=datetime.utcnow)
  expiration_date = db.Column(DATE(), nullable=False)

  # 'states' field in StockItem instance is sqlalchemy query object which can
  # be used to specify whether or not to grab all previous 'StockItemState's (a lot)
  # or just the most recent one...or something else
  states = db.relationship('StockItemState', lazy='dynamic', backref=db.backref('food_item', lazy=True))
  food_kind = db.relationship('FoodKind', lazy='joined')

  def full_dict(self):
    current_state = self.states.order_by(text('date_created desc')).first()
    return {
      **self.cols_dict(),
      'food_kind': self.food_kind,
      'current_state': current_state.full_dict() if current_state else None,
    }
