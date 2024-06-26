"""empty message

Revision ID: 924e64a0c3d9
Revises: 9f7db7201559
Create Date: 2024-06-09 14:14:31.140628

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '924e64a0c3d9'
down_revision = '9f7db7201559'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('material_list', schema=None) as batch_op:
        batch_op.drop_constraint('material_list_ibfk_1', type_='foreignkey')
        batch_op.drop_column('fk_product_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('material_list', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fk_product_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('material_list_ibfk_1', 'product_list', ['fk_product_id'], ['id'])

    # ### end Alembic commands ###
