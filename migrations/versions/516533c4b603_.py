"""empty message

Revision ID: 516533c4b603
Revises: c8a06106de8d
Create Date: 2024-06-10 16:52:01.381153

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '516533c4b603'
down_revision = 'c8a06106de8d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_created', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('date_modified', sa.DateTime(), nullable=True))
        batch_op.drop_column('date_added')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_added', mysql.DATETIME(), nullable=True))
        batch_op.drop_column('date_modified')
        batch_op.drop_column('date_created')

    # ### end Alembic commands ###
