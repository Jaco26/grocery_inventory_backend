from sqlalchemy.dialects.postgresql import UUID

from app.database.db import db
from app.database.mixins import TimestampMixin


class StockItemState(TimestampMixin, db.Model):
  stock_item_id = db.Column(UUID(as_uuid=True), db.ForeignKey('stock_item.id'))
  packaging_kind_id = db.Column(UUID(as_uuid=True), db.ForeignKey('packaging_kind.id'))
  packaging_state_id = db.Column(UUID(as_uuid=True), db.ForeignKey('packaging_state.id'))
  quantity = db.Column(db.Integer, default=0)
  
  # has lazy loaded 'backref'ed relationship field 'food_item'

  packaging_kind = db.relationship('PackagingKind', lazy='joined')
  packaging_state = db.relationship('PackagingState', lazy='joined')

  def full_dict(self):
    remove = ['packaging_kind_id', 'packaging_state_id']
    return {
      **{ key: getattr(self, key) for key in self.cols_dict().keys() if key not in remove },
      'packaging_kind': self.packaging_kind,
      'packaging_state': self.packaging_state
    }