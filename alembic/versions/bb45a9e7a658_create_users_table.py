"""create users table

Revision ID: bb45a9e7a658
Revises: 
Create Date: 2023-05-18 13:11:46.265288

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func
import uuid

# revision identifiers, used by Alembic.
revision = 'bb45a9e7a658'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column('id', sa.String(), primary_key=True, default=uuid.uuid4),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column('modified_at', sa.DateTime(timezone=True), server_onupdate=func.now()),
    )


def downgrade() -> None:
    op.drop_table('users')
