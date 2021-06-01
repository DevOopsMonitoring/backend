"""empty message

Revision ID: 53a4974865c1
Revises: be331add6aec
Create Date: 2021-05-31 19:14:50.123652

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53a4974865c1'
down_revision = 'be331add6aec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('read_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('server_id', sa.Integer(), nullable=False),
    sa.Column('sensor_id', sa.Integer(), nullable=False),
    sa.Column('value', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['sensor_id'], ['sensor.id'], ),
    sa.ForeignKeyConstraint(['server_id'], ['server.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('read_data')
    # ### end Alembic commands ###