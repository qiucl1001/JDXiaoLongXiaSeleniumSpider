"""initial migration

Revision ID: 1fe87e7cc90f
Revises: 
Create Date: 2020-04-16 23:28:43.890986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fe87e7cc90f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('jd_xlx',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('price', sa.String(length=32), nullable=True),
    sa.Column('desc', sa.Text(), nullable=True),
    sa.Column('comments', sa.String(length=32), nullable=True),
    sa.Column('shop', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('jd_xlx')
    # ### end Alembic commands ###
