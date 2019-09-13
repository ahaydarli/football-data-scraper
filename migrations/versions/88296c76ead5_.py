"""empty message

Revision ID: 88296c76ead5
Revises: 4aa207b9ffbe
Create Date: 2019-07-08 07:05:31.340734

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88296c76ead5'
down_revision = '4aa207b9ffbe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('country',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('country_id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_password'), 'user', ['password'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('leagues',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('league_id', sa.Integer(), nullable=True),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['country.country_id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('country_id'),
    sa.UniqueConstraint('league_id')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_timestamp'), 'post', ['timestamp'], unique=False)
    op.create_table('year',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('league_id', sa.Integer(), nullable=True),
    sa.Column('url', sa.String(length=200), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('code', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['league_id'], ['leagues.league_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('club',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.Column('league_id', sa.Integer(), nullable=True),
    sa.Column('year_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('code', sa.String(length=100), nullable=True),
    sa.Column('url', sa.String(length=200), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['country.country_id'], ),
    sa.ForeignKeyConstraint(['league_id'], ['leagues.league_id'], ),
    sa.ForeignKeyConstraint(['year_id'], ['year.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('week',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('year_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('url', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['year_id'], ['year.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('week_clubs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('code', sa.String(length=100), nullable=True),
    sa.Column('url', sa.String(length=200), nullable=True),
    sa.Column('year_id', sa.Integer(), nullable=True),
    sa.Column('week_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['week_id'], ['week.id'], ),
    sa.ForeignKeyConstraint(['year_id'], ['year.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('week_clubs')
    op.drop_table('week')
    op.drop_table('club')
    op.drop_table('year')
    op.drop_index(op.f('ix_post_timestamp'), table_name='post')
    op.drop_table('post')
    op.drop_table('leagues')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_password'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('country')
    # ### end Alembic commands ###
