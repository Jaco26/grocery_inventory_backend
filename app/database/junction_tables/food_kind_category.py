from sqlalchemy.dialects.postgresql import UUID

from app.database.db import db


food_kind_category = db.Table('food_kind_category',
  db.Column('food_kind_id', db.ForeignKey('food_kind.id'), primary_key=True),
  db.Column('food_category_id', db.ForeignKey('food_category.id'), primary_key=True),
)
