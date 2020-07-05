"""initial

Revision ID: 5732c79f2cea
Revises: 
Create Date: 2020-07-05 13:24:26.628561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5732c79f2cea'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('channel',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('video',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('added_at', sa.DateTime(), nullable=True),
    sa.Column('channel_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['channel_id'], ['channel.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('video')
    op.drop_table('channel')
    # ### end Alembic commands ###
