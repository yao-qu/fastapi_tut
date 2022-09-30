"""add content to posts table

Revision ID: d3461411c7f4
Revises: 8e3f54d6c1de
Create Date: 2022-09-30 20:04:15.287274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3461411c7f4'
down_revision = '8e3f54d6c1de'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
