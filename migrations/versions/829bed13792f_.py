"""empty message

Revision ID: 829bed13792f
Revises: b4eb39a95790
Create Date: 2022-03-21 11:53:16.379445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '829bed13792f'
down_revision = 'b4eb39a95790'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tracking',
    sa.Column('created', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=200), nullable=True),
    sa.Column('comments', sa.String(length=240), nullable=True),
    sa.Column('incident_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['incident_id'], ['incident.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tracking')
    # ### end Alembic commands ###
