"""initial

Revision ID: 763e3f8d7028
Revises: None
Create Date: 2025-07-21 00:00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '763e3f8d7028'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=100), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.UniqueConstraint('email', name='uq_users_email')
    )
    # Create articles table
    op.create_table('articles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('meta_description', sa.String(length=300)),
        sa.Column('image_prompt', sa.Text()),
        sa.Column('image_url', sa.Text()),
        sa.Column('wordpress_id', sa.Integer()),
        sa.Column('wordpress_url', sa.String(length=500)),
        sa.Column('published_at', sa.DateTime()),
        sa.Column('twitter_posted_at', sa.DateTime()),
        sa.Column('instagram_posted_at', sa.DateTime()),
        sa.Column('created_at', sa.DateTime(), nullable=False)
    )
    # Create feedback table
    op.create_table('feedback',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('email', sa.String(length=255)),
        sa.Column('name', sa.String(length=100)),
        sa.Column('resolved', sa.Boolean(), nullable=False),
        sa.Column('resolved_at', sa.DateTime()),
        sa.Column('created_at', sa.DateTime(), nullable=False)
    )
    # Create analytics table
    op.create_table('analytics',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('event_type', sa.String(length=50), nullable=False),
        sa.Column('event_data', sa.Text()),
        sa.Column('created_at', sa.DateTime(), nullable=False)
    )
    # Create versions table (depends on articles)
    op.create_table('versions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('article_id', sa.Integer(), sa.ForeignKey('articles.id', ondelete='CASCADE'), nullable=False),
        sa.Column('diff', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False)
    )

def downgrade():
    # Drop tables in reverse order of creation (consider foreign key dependencies)
    op.drop_table('versions')
    op.drop_table('analytics')
    op.drop_table('feedback')
    op.drop_table('articles')
    op.drop_table('users')
