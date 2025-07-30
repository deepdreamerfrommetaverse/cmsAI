"""seed initial data"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime
from passlib.hash import bcrypt

revision = "111111111111"
down_revision = "763e3f8d7028"
branch_labels = None
depends_on = None

def upgrade() -> None:
    conn = op.get_bind()
    insert_stmt = sa.text("""
        INSERT INTO users (email, hashed_password, role, created_at)
        VALUES (:email, :pwd, 'admin', :ts)
        ON CONFLICT (email) DO NOTHING
    """)
    conn.execute(insert_stmt, {
        "email": "admin@example.com",
        "pwd": bcrypt.hash("Radek125r!"),
        "ts":  datetime.utcnow()
    })

def downgrade() -> None:
    op.execute(
        sa.text("DELETE FROM users WHERE email = :email"),
        {"email": "admin@example.com"},
    )
