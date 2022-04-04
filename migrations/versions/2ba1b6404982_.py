"""empty message

Revision ID: 2ba1b6404982
Revises: b95eb5a9c0bd
Create Date: 2022-04-04 15:14:57.229501

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ba1b6404982'
down_revision = 'b95eb5a9c0bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vehicle',
    sa.Column('created', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('make', sa.String(length=150), nullable=True),
    sa.Column('model', sa.String(length=240), nullable=True),
    sa.Column('category', sa.String(length=200), nullable=True),
    sa.Column('year', sa.String(length=50), nullable=True),
    sa.Column('transmision', sa.String(length=120), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vehicle')
    # ### end Alembic commands ###
