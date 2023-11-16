"""initial migration

Revision ID: fc880adcd038
Revises: 55276f884f7e
Create Date: 2023-11-16 18:50:11.123024

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc880adcd038'
down_revision: Union[str, None] = '55276f884f7e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
