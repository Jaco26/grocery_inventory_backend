from sqlalchemy.dialects.postgresql import UUID

from app.database.db import db
from app.database.mixins import TimestampMixin


class Snapshot(TimestampMixin, db.Model):
  stock_id = db.Column(UUID(as_uuid=True), db.ForeignKey('stock.id'))
  food_item_states = db.relationship('FoodItemState', secondary='snapshot_food_item_state', lazy='subquery')