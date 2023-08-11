"""Add URL column to Asset table

Revision ID: a9cfca60f7fc
Revises: ed1c9b031630
Create Date: 2023-08-10 22:48:32.666881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9cfca60f7fc'
down_revision = 'ed1c9b031630'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('asset', schema=None) as batch_op:
        batch_op.add_column(sa.Column('url', sa.String(length=256), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('asset', schema=None) as batch_op:
        batch_op.drop_column('url')

    # ### end Alembic commands ###
