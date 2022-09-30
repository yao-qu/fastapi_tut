"""add foreign key to post table

Revision ID: a0feedcc5b29
Revises: c29c8057fcee
Create Date: 2022-09-30 21:04:06.097332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0feedcc5b29'
down_revision = 'c29c8057fcee'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable = False))
    op.create_foreign_key('post_users_fk', source_table = 'posts', referent_table = 'users', local_cols = ['owner_id'], 
    remote_cols = ['id'], ondelete = 'CASCADE')


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name ="posts")
    op.drop_column('posts', 'owner_id')
