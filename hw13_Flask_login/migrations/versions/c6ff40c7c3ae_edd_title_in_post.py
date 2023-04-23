"""edd title in Post

Revision ID: c6ff40c7c3ae
Revises: 11b248b5c1a1
Create Date: 2023-04-23 17:18:31.062038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6ff40c7c3ae'
down_revision = '11b248b5c1a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_column('title')

    # ### end Alembic commands ###
