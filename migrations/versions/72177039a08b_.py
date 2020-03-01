"""empty message

Revision ID: 72177039a08b
Revises: 1e2e5bff5272
Create Date: 2020-03-01 17:08:55.561092

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '72177039a08b'
down_revision = '1e2e5bff5272'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('revoked_token',
    sa.Column('jti', postgresql.UUID(as_uuid=True), nullable=False),
    sa.PrimaryKeyConstraint('jti')
    )
    op.add_column('food_item', sa.Column('date_created', postgresql.TIMESTAMP(timezone=True), nullable=True))
    op.add_column('food_item', sa.Column('date_updated', postgresql.TIMESTAMP(timezone=True), nullable=True))
    op.add_column('stock', sa.Column('name', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'stock', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'stock', type_='unique')
    op.drop_column('stock', 'name')
    op.drop_column('food_item', 'date_updated')
    op.drop_column('food_item', 'date_created')
    op.drop_table('revoked_token')
    # ### end Alembic commands ###
