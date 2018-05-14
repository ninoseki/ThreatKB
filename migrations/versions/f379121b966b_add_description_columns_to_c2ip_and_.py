"""Add description columns to c2ip and c2dns

Revision ID: f379121b966b
Revises: 658ab905b871
Create Date: 2018-05-13 23:18:31.422992

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f379121b966b'
down_revision = '658ab905b871'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('c2dns', sa.Column('description', sa.String(length=512), nullable=True))
    op.add_column('c2ip', sa.Column('description', sa.String(length=512), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('c2ip', 'description')
    op.drop_column('c2dns', 'description')
    # ### end Alembic commands ###
