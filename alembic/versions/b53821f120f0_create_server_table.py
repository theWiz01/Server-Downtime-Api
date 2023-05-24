"""create server table

Revision ID: b53821f120f0
Revises: bb45a9e7a658
Create Date: 2023-05-19 20:29:26.531910

"""
from alembic import op
import sqlalchemy as sa
import uuid
from sqlalchemy.sql import func
# revision identifiers, used by Alembic.
revision = 'b53821f120f0'
down_revision = 'bb45a9e7a658'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "servers",
        sa.Column('id', sa.String(), default=uuid.uuid4, primary_key=True),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column('modified_at', sa.DateTime(timezone=True), server_onupdate=func.now())
    )


def downgrade() -> None:
    op.drop_table("servers")
