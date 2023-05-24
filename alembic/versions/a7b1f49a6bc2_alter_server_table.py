"""alter server table

Revision ID: a7b1f49a6bc2
Revises: b53821f120f0
Create Date: 2023-05-20 23:24:41.523758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7b1f49a6bc2'
down_revision = 'b53821f120f0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("servers", 
        sa.Column("active", sa.BOOLEAN, default=True)
    )


def downgrade() -> None:
    op.drop_column("servers", sa.Column("active"))
