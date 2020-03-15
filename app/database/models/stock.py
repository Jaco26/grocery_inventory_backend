from sqlalchemy.dialects.postgresql import UUID

from app.database.db import db
from app.database.mixins import TimestampMixin


class Stock(TimestampMixin, db.Model):
  user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('app_user.id'))
  name = db.Column(db.String, nullable=False)
  uniform_name = db.Column(db.String, nullable=False, unique=True)

  # each snapshot is a collection of 'food_item_state's. a snapshot
  # represents the state of a 'stock' at a given moment in time
  snapshots = db.relationship('Snapshot', lazy='dynamic',
                              backref=db.backref('stock', lazy=True))

  # represents the 'food_item's in a 'stock'
  food_items = db.relationship('FoodItem', lazy='joined')
    
  def full_dict(self):
    return {
      **self.cols_dict(),
      'snapshots': [s for s in self.snapshots.all()],
      'items': [item.full_dict() for item in self.food_items]
    }