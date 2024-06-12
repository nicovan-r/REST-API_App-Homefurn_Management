"""New Table: product_list

Revision ID: 585f7a0b329c
Revises: ab0e4c836a4a
Create Date: 2024-06-08 10:52:43.165508

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '585f7a0b329c'
down_revision = 'ab0e4c836a4a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('storage_location', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_created', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('date_modified', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('storage_location', schema=None) as batch_op:
        batch_op.drop_column('date_modified')
        batch_op.drop_column('date_created')

    # ### end Alembic commands ###