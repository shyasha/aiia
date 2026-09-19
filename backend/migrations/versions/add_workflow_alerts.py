"""add workflow_alerts table

Revision ID: e2f3a4b5c6d7
Revises: d1a2b3c4d5e6
Create Date: 2026-09-19 03:05:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'e2f3a4b5c6d7'
down_revision: Union[str, Sequence[str], None] = 'd1a2b3c4d5e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create workflow_alerts table for the AI Co-Pilot feature."""
    op.create_table(
        'workflow_alerts',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('entity_type', sa.String(20), nullable=False),
        sa.Column('entity_id', sa.String(36), nullable=False),
        sa.Column('alert_type', sa.String(30), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('severity', sa.String(10), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_workflow_alerts_entity_id', 'workflow_alerts', ['entity_id'])
    op.create_index('ix_workflow_alerts_severity', 'workflow_alerts', ['severity'])


def downgrade() -> None:
    """Drop workflow_alerts table."""
    op.drop_index('ix_workflow_alerts_severity', table_name='workflow_alerts')
    op.drop_index('ix_workflow_alerts_entity_id', table_name='workflow_alerts')
    op.drop_table('workflow_alerts')
