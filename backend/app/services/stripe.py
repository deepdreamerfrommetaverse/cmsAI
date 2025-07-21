import stripe as stripe_sdk
from app.core.config import get_settings

settings = get_settings()
if settings.STRIPE_SECRET_KEY:
    stripe_sdk.api_key = settings.STRIPE_SECRET_KEY

async def get_revenue():
    if not settings.STRIPE_SECRET_KEY:
        return {"revenue": 0}
    # last 30 days charges total
    charges = stripe_sdk.Charge.list(created={'gte': int(stripe_sdk.util.utcnow().timestamp()) - 30*24*3600})
    amount = sum(c.amount for c in charges.auto_paging_iter())
    return {"revenue": amount / 100}
