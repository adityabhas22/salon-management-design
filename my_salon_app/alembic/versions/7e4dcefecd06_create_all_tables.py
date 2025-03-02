"""Create all tables

Revision ID: 7e4dcefecd06
Revises: 75d38e7178e8
Create Date: 2025-02-28 19:37:03.554811

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e4dcefecd06'
down_revision: Union[str, None] = '75d38e7178e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
