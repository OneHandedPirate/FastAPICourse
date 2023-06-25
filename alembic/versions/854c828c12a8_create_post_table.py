"""create post table

Revision ID: 854c828c12a8
Revises: 
Create Date: 2023-06-25 15:36:04.449290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '854c828c12a8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('post', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table('post')
