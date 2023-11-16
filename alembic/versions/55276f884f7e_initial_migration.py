"""initial migration

Revision ID: 55276f884f7e
Revises: 6ebff59bc569
Create Date: 2023-11-16 18:47:52.977214

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '55276f884f7e'
down_revision: Union[str, None] = '6ebff59bc569'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
