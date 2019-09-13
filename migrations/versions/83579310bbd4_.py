"""empty message

Revision ID: 83579310bbd4
Revises: 2a8225c633a1
Create Date: 2019-07-07 22:01:40.235783

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83579310bbd4'
down_revision = '2a8225c633a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('club', sa.Column('code', sa.String(length=100), nullable=True))
    op.add_column('club', sa.Column('url', sa.String(length=200), nullable=True))
    op.create_foreign_key(None, 'club', 'year', ['year_id'], ['id'])
    op.drop_constraint(None, 'leagues', type_='foreignkey')
    op.create_foreign_key(None, 'leagues', 'country', ['country_id'], ['country_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'leagues', type_='foreignkey')
    op.create_foreign_key(None, 'leagues', 'country', ['country_id'], ['id'])
    op.drop_constraint(None, 'club', type_='foreignkey')
    op.drop_column('club', 'url')
    op.drop_column('club', 'code')
    # ### end Alembic commands ###
