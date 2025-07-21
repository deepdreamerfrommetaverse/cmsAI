"""add social_limits

Revision ID: 0003
Revises: 0002
Create Date: 2025-07-18
"""
from alembic import op
import sqlalchemy as sa

revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('social_limits',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('service', sa.String(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('count', sa.Integer(), nullable=True),
        sa.Column('limit', sa.Integer(), nullable=False),
        sa.UniqueConstraint('service', 'date', name='uix_service_date'),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('social_limits')
