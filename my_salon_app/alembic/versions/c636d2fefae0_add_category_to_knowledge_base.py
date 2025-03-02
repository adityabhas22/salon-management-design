"""add_category_to_knowledge_base

Revision ID: c636d2fefae0
Revises: 54ea417e565c
Create Date: 2025-02-28 20:39:21.564227

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c636d2fefae0'
down_revision: Union[str, None] = '54ea417e565c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add category column to knowledge_base table
    op.add_column('knowledge_base', sa.Column('category', sa.String(), nullable=True))


def downgrade() -> None:
    # Remove category column from knowledge_base table
    op.drop_column('knowledge_base', 'category')
