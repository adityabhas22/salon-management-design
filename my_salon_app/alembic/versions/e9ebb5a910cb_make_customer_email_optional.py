"""Make customer email optional

Revision ID: e9ebb5a910cb
Revises: c636d2fefae0
Create Date: 2025-03-01 13:57:23.526859

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9ebb5a910cb'
down_revision: Union[str, None] = 'c636d2fefae0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Make email column nullable
    op.alter_column('customers', 'email',
               existing_type=sa.String(),
               nullable=True)


def downgrade() -> None:
    # Revert email column to non-nullable
    op.alter_column('customers', 'email',
               existing_type=sa.String(),
               nullable=False)
