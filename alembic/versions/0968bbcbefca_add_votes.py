"""add votes

Revision ID: 0968bbcbefca
Revises: 676d33a4ece6
Create Date: 2023-06-25 16:21:31.777201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0968bbcbefca'
down_revision = '676d33a4ece6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vote',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    op.add_column('post', sa.Column('author_id', sa.Integer(), nullable=False))
    op.drop_constraint('post_user_fk', 'post', type_='foreignkey')
    op.create_foreign_key(None, 'post', 'user', ['author_id'], ['id'], ondelete='CASCADE')
    op.drop_column('post', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.create_foreign_key('post_user_fk', 'post', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_column('post', 'author_id')
    op.drop_table('vote')
    # ### end Alembic commands ###
