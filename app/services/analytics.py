from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
# Placeholder – implement pageview/event tracking here. For demo returns empty stats.
async def get_stats(db: AsyncSession):
    return {"pageviews": 0, "events": 0, "timestamp": datetime.utcnow().isoformat()}
