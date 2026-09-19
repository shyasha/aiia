"""drop ai risk fields from adverse events

Revision ID: d1a2b3c4d5e6
Revises: c4971b361024
Create Date: 2026-09-19 03:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'd1a2b3c4d5e6'
down_revision: Union[str, Sequence[str], None] = 'c4971b361024'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Drop AI clinical risk fields — replaced by workflow_alerts table."""
    op.drop_column('adverse_events', 'ai_flagged_at')
    op.drop_column('adverse_events', 'ai_reasoning')
    op.drop_column('adverse_events', 'ai_risk_level')


def downgrade() -> None:
    """Restore AI clinical risk fields."""
    op.add_column('adverse_events', sa.Column('ai_risk_level', sa.String(length=20), nullable=True))
    op.add_column('adverse_events', sa.Column('ai_reasoning', sa.Text(), nullable=True))
    op.add_column('adverse_events', sa.Column('ai_flagged_at', sa.DateTime(), nullable=True))
