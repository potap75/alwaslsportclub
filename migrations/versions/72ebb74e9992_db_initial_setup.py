"""db initial setup

Revision ID: 72ebb74e9992
Revises: 
Create Date: 2023-04-22 01:20:14.860582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72ebb74e9992'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('person',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group', sa.String(length=10), nullable=True),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('mobile', sa.String(length=10), nullable=True),
    sa.Column('nationality', sa.String(length=20), nullable=True),
    sa.Column('department', sa.String(length=20), nullable=True),
    sa.Column('position', sa.String(length=20), nullable=True),
    sa.Column('team', sa.String(length=20), nullable=True),
    sa.Column('sport', sa.String(length=250), nullable=True),
    sa.Column('image', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    op.drop_table('person')
    # ### end Alembic commands ###
