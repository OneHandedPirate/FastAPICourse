"""create content column

Revision ID: f4016ab870e7
Revises: 854c828c12a8
Create Date: 2023-06-25 15:45:01.662764

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4016ab870e7'
down_revision = '854c828c12a8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('post', sa.Column('content', sa.String, nullable=False))


def downgrade() -> None:
    op.drop_column('post', 'content')
