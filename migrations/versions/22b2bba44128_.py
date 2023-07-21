"""empty message

Revision ID: 22b2bba44128
Revises: 
Create Date: 2023-07-20 23:23:19.605851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22b2bba44128'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Order_id', sa.Integer(), autoincrement=True, nullable=False))
        batch_op.add_column(sa.Column('watch_mid', sa.String(length=20), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_orders_watch_mid_watches'), 'watches', ['watch_mid'], ['watch_mid'])
        batch_op.drop_column('id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.INTEGER(), nullable=False))
        batch_op.drop_constraint(batch_op.f('fk_orders_watch_mid_watches'), type_='foreignkey')
        batch_op.drop_column('watch_mid')
        batch_op.drop_column('Order_id')

    # ### end Alembic commands ###
