"""create tables

Revision ID: 7eca646be037
Revises: 7e4dcefecd06
Create Date: 2025-02-28 20:04:29.011467

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7eca646be037'
down_revision: Union[str, None] = '7e4dcefecd06'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
