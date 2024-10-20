"""Add image_filename to Tour

Revision ID: ba6f6db5b18d
Revises: c0b34b3adbfb
Create Date: 2024-10-20 22:56:15.214381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba6f6db5b18d'
down_revision = 'c0b34b3adbfb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tour', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_filename', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tour', schema=None) as batch_op:
        batch_op.drop_column('image_filename')

    # ### end Alembic commands ###
