from sqlalchemy.dialects.postgresql import UUID

from app.database.db import db
from app.database.mixins import TimestampMixin, UserDefinedNameMixin


class Stock(TimestampMixin, UserDefinedNameMixin, db.Model):
  user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('app_user.id'))

  # each snapshot is a collection of 'stock_item_state's. a snapshot
  # represents the state of a 'stock' at a given moment in time
  snapshots = db.relationship('Snapshot', lazy='dynamic',
                              backref=db.backref('stock', lazy=True))

  # represents the 'food_item's in a 'stock'
  stock_items = db.relationship('StockItem', lazy='joined')

  def __init__(self, **kwargs):
    super(Stock, self).__init__(**kwargs)
    self.user_id = kwargs.get('user_id')
    
  def full_dict(self):
    return {
      **self.cols_dict(),
      'snapshots': [s for s in self.snapshots.all()],
      'items': [item.full_dict() for item in self.stock_items]
    }