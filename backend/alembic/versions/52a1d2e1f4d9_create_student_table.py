"""Create Student table

Revision ID: 52a1d2e1f4d9
Revises: 
Create Date: 2025-12-01 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# revision identifiers, used by Alembic.
revision = '52a1d2e1f4d9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'students',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True),
        sa.Column('name', sa.String(), index=True, nullable=True),
        sa.Column('email', sa.String(), unique=True, index=True, nullable=False),
        sa.Column('software_background', sa.String(), nullable=True),
        sa.Column('hardware_background', sa.String(), nullable=True),
        sa.Column('language_preference', sa.String(), nullable=True),
    )


def downgrade():
    op.drop_table('students')

