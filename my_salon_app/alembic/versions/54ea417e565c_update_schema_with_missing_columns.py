"""update_schema_with_missing_columns

Revision ID: 54ea417e565c
Revises: 7eca646be037
Create Date: 2025-02-28 20:07:58.389126

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54ea417e565c'
down_revision: Union[str, None] = '7eca646be037'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add duration_minutes column to services table
    op.add_column('services', sa.Column('duration_minutes', sa.Integer(), nullable=False, server_default='60'))
    
    # Add start_date column to promotions table
    op.add_column('promotions', sa.Column('start_date', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))


def downgrade() -> None:
    # Remove added columns
    op.drop_column('services', 'duration_minutes')
    op.drop_column('promotions', 'start_date')
