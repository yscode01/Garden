"""Add tags column to post

Revision ID: 94689883aa37
Revises: 471666440c68
Create Date: 2024-06-13 08:30:11.705664

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94689883aa37'
down_revision = '471666440c68'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('post') as batch_op:
        batch_op.add_column(sa.Column('tags', sa.String(), nullable=False))


def downgrade():
    with op.batch_alter_table('post') as batch_op:
        batch_op.drop_column('tags')
