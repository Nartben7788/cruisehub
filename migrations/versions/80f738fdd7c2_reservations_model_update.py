"""Reservations model update

Revision ID: 80f738fdd7c2
Revises: 8d8a0c672c19
Create Date: 2024-02-10 13:09:06.395322

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80f738fdd7c2'
down_revision = '8d8a0c672c19'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservations', schema=None) as batch_op:
        batch_op.drop_column('status')

    # ### end Alembic commands ###
