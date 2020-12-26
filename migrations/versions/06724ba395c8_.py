"""empty message

Revision ID: 06724ba395c8
Revises: 2b056b8f811e
Create Date: 2020-12-26 18:23:26.120095

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06724ba395c8'
down_revision = '2b056b8f811e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('hashed_password', sa.String(length=128), nullable=True),
    sa.Column('first_name', sa.String(length=32), nullable=False),
    sa.Column('last_name', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
