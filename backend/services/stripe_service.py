import stripe
from fastapi import HTTPException

from core.settings import settings

def get_revenue():
    """Fetch total revenue from Stripe (sums of all successful charges by currency)."""
    if not settings.stripe_api_key:
        raise HTTPException(status_code=503, detail="Stripe integration not configured")
    # Use global stripe.api_key set in startup
    try:
        total_by_currency = {}
        charges = stripe.Charge.list(limit=100, status="succeeded")
        # Iterate through all charges using auto pagination
        for charge in charges.auto_paging_iter():
            cur = charge.currency.upper()
            amt = charge.amount  # amount in smallest currency unit (cents)
            total_by_currency[cur] = total_by_currency.get(cur, 0) + amt
    except stripe.error.AuthenticationError:
        raise HTTPException(status_code=502, detail="Stripe authentication failed")
    except stripe.error.StripeError as e:
        # Use user_message if available for a more user-friendly error
        msg = getattr(e, "user_message", str(e))
        raise HTTPException(status_code=502, detail=f"Stripe API error: {msg}")
    # Prepare results
    revenue_items = []
    for currency, cents in total_by_currency.items():
        amount = cents / 100.0
        # Round to 2 decimal places for currency
        amount = round(amount, 2)
        revenue_items.append({"currency": currency, "total": amount})
    return revenue_items
