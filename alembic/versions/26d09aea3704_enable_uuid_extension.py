"""Enable uuid extension

Revision ID: 26d09aea3704
Revises:
Create Date: 2018-06-07 17:01:53.004325

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26d09aea3704'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    connection.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')


def downgrade():
    connection = op.get_bind()
    connection.execute("DROP EXTENSION IF EXISTS 'uuid-ossp'")
