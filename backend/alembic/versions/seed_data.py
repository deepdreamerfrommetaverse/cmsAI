"""seed initial data

Revision ID: 111111111111
Revises: 763e3f8d7028
"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime
from passlib.hash import bcrypt
from core.settings import settings         # ← klasa BaseSettings

revision = "111111111111"
down_revision = "763e3f8d7028"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()

    insert_stmt = sa.text("""
        INSERT INTO users (email, hashed_password, role, created_at)
        VALUES (:email, :pwd, 'admin', :ts)
        ON CONFLICT (email) DO NOTHING        -- idempotent
    """)

    conn.execute(insert_stmt, {
        "email": settings.admin_email,
        "pwd": bcrypt.hash(settings.admin_password),
        "ts":  datetime.utcnow()
    })


def downgrade() -> None:
    op.execute(
        sa.text("DELETE FROM users WHERE email = :email"),
        {"email": settings.admin_email},
    )
