from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.analytics_event import AnalyticsEvent

async def track_event(db: AsyncSession, path: str, event_type: str = "pageview"):
    ev = AnalyticsEvent(path=path, event_type=event_type)
    db.add(ev)
    await db.commit()

async def get_stats(db: AsyncSession):
    # last 7 days
    since = datetime.utcnow() - timedelta(days=7)
    stmt = (
        select(
            func.date_trunc('day', AnalyticsEvent.created_at).label('day'),
            func.count().label('views')
        )
        .where(AnalyticsEvent.created_at >= since)
        .group_by('day')
        .order_by('day')
    )
    res = await db.execute(stmt)
    days = [{"date": row.day.strftime("%Y-%m-%d"), "views": row.views} for row in res]
    total = sum(d["views"] for d in days)
    return {"total": total, "by_day": days}
