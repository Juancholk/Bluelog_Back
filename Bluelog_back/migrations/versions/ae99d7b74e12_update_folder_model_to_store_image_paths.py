"""Update Folder model to store image paths

Revision ID: ae99d7b74e12
Revises: d483faead6f2
Create Date: 2024-09-09 23:20:57.425269

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae99d7b74e12'
down_revision = 'd483faead6f2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('folder', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_path', sa.String(length=255), nullable=True))
        batch_op.drop_column('image_data')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('folder', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_data', sa.BLOB(), nullable=True))
        batch_op.drop_column('image_path')

    # ### end Alembic commands ###
