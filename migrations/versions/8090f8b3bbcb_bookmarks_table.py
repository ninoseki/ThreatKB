"""bookmarks table

Revision ID: 8090f8b3bbcb
Revises: 665baa4d3f57
Create Date: 2017-11-12 21:50:21.374017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8090f8b3bbcb'
down_revision = '665baa4d3f57'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bookmarks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('entity_type', sa.Integer(), nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['kb_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(u'ix_bookmarks_entity_id', 'bookmarks', ['entity_id'], unique=False)
    op.create_index(u'ix_bookmarks_entity_type', 'bookmarks', ['entity_type'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(u'ix_bookmarks_entity_type', table_name='bookmarks')
    op.drop_index(u'ix_bookmarks_entity_id', table_name='bookmarks')
    op.drop_table('bookmarks')
    # ### end Alembic commands ###
