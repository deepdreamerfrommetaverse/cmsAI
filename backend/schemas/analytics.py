from typing import Optional, Union, Dict
from pydantic import BaseModel

class AnalyticsEventCreate(BaseModel):
    event_type: str
    event_data: Optional[Union[str, Dict]] = None

class AnalyticsSummary(BaseModel):
    total_events: int
    page_views: int
    events_by_type: Dict[str, int]
