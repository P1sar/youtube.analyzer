"""description

Revision ID: 591372ec0eae
Revises: 5732c79f2cea
Create Date: 2020-07-05 18:15:59.467501

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '591372ec0eae'
down_revision = '5732c79f2cea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('video', sa.Column('description', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('video', 'description')
    # ### end Alembic commands ###