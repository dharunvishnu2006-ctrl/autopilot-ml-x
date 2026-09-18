"""add hyperparams jsonb to runs

Revision ID: 678aecb097cb
Revises:
Create Date: 2026-09-18 11:57:04.677620

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "678aecb097cb"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("runs", sa.Column("notes_v2", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("runs", "notes_v2")
