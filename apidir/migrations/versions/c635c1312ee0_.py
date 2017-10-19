"""empty message

Revision ID: c635c1312ee0
Revises: 
Create Date: 2017-10-18 21:42:32.376798

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c635c1312ee0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=140), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pacts_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pact_id', sa.Integer(), nullable=True),
    sa.Column('user_username', sa.String(length=20), nullable=True),
    sa.Column('pact_signed', sa.Integer(), nullable=False),
    sa.Column('conditions_passed', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('conditions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pact_id', sa.Integer(), nullable=True),
    sa.Column('doer_username', sa.String(length=20), nullable=False),
    sa.Column('issuer_username', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['pact_id'], ['pacts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('conditions')
    op.drop_table('users')
    op.drop_table('pacts_users')
    op.drop_table('pacts')
    # ### end Alembic commands ###
