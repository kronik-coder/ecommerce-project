"""empty message

Revision ID: 122e6988f823
Revises: a2f35c47c5e9
Create Date: 2021-11-06 19:05:52.846190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '122e6988f823'
down_revision = 'a2f35c47c5e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book_name', sa.String(length=200), nullable=True),
    sa.Column('genre', sa.String(length=200), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('books')
    # ### end Alembic commands ###