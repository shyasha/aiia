"""add suspected_causative_drug_id to adverse_events

Revision ID: f1e2d3c4b5a6
Revises: e2f3a4b5c6d7
Create Date: 2026-09-19 03:26:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'f1e2d3c4b5a6'
down_revision: Union[str, Sequence[str], None] = 'e2f3a4b5c6d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add manually-entered suspected causative drug FK to adverse_events.

    Uses batch mode so this works on both SQLite (dev) and PostgreSQL (prod).
    """
    with op.batch_alter_table('adverse_events') as batch_op:
        batch_op.add_column(
            sa.Column('suspected_causative_drug_id', sa.String(length=36), nullable=True),
        )
        batch_op.create_foreign_key(
            'fk_ae_suspected_drug',
            'interventions',
            ['suspected_causative_drug_id'],
            ['id'],
            ondelete='SET NULL',
        )


def downgrade() -> None:
    """Remove suspected_causative_drug_id from adverse_events."""
    with op.batch_alter_table('adverse_events') as batch_op:
        batch_op.drop_constraint('fk_ae_suspected_drug', type_='foreignkey')
        batch_op.drop_column('suspected_causative_drug_id')
