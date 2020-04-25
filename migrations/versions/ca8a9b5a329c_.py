"""empty message

Revision ID: ca8a9b5a329c
Revises: a5c81a8e5dea
Create Date: 2020-04-25 14:21:40.453847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca8a9b5a329c'
down_revision = 'a5c81a8e5dea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('food_category_uniform_name_key', 'food_category', type_='unique')
    op.drop_constraint('food_kind_uniform_name_key', 'food_kind', type_='unique')
    op.drop_constraint('packaging_kind_uniform_name_key', 'packaging_kind', type_='unique')
    op.drop_constraint('packaging_state_uniform_name_key', 'packaging_state', type_='unique')
    op.drop_constraint('stock_uniform_name_key', 'stock', type_='unique')
    op.drop_constraint('unit_of_measurement_uniform_name_key', 'unit_of_measurement', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('unit_of_measurement_uniform_name_key', 'unit_of_measurement', ['uniform_name'])
    op.create_unique_constraint('stock_uniform_name_key', 'stock', ['uniform_name'])
    op.create_unique_constraint('packaging_state_uniform_name_key', 'packaging_state', ['uniform_name'])
    op.create_unique_constraint('packaging_kind_uniform_name_key', 'packaging_kind', ['uniform_name'])
    op.create_unique_constraint('food_kind_uniform_name_key', 'food_kind', ['uniform_name'])
    op.create_unique_constraint('food_category_uniform_name_key', 'food_category', ['uniform_name'])
    # ### end Alembic commands ###