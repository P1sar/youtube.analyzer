"""videos.parsed_at.added

Revision ID: 5fc550271bb2
Revises: 2b5160bcd04a
Create Date: 2020-08-16 13:57:40.366722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fc550271bb2'
down_revision = '2b5160bcd04a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('video', sa.Column('parsed_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('video', 'parsed_at')
    # ### end Alembic commands ###
