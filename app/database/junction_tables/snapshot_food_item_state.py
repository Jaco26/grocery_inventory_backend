from sqlalchemy.dialects.postgresql import UUID

from app.database.db import db


snapshot_food_item_state = db.Table('snapshot_food_item_state',
  db.Column('snapshot_id', db.ForeignKey('snapshot.id'), primary_key=True),
  db.Column('food_item_state_id', db.ForeignKey('food_item_state.id'), primary_key=True),
)