"""Add reset_token column to User and Owner models

Revision ID: 33c42482b9e4
Revises: f12709be3565
Create Date: 2024-02-21 15:11:34.393265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33c42482b9e4'
down_revision = 'f12709be3565'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('owner', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reset_token', sa.String(), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reset_token', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('reset_token')

    with op.batch_alter_table('owner', schema=None) as batch_op:
        batch_op.drop_column('reset_token')

    # ### end Alembic commands ###
