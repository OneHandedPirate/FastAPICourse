"""add foreign key to post table

Revision ID: ad001389d62c
Revises: afece550b2ca
Create Date: 2023-06-25 16:00:52.597704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad001389d62c'
down_revision = 'afece550b2ca'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('post', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key('post_user_fk', source_table="post", referent_table='user',
                          local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('post_user_fk', table_name='post')
    op.drop_column('post', 'user_id')
    pass
