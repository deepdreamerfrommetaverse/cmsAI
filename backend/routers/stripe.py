from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from services import stripe_service
from core.auth import get_current_admin

router = APIRouter()

@router.get("/revenue")
def get_revenue(db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    """Retrieve revenue summary from Stripe (admin only)."""
    data = stripe_service.get_revenue()
    return data
