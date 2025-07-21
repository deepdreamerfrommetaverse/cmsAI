import pytest
from app.core.scheduler import start, scheduler

@pytest.mark.anyio
async def test_scheduler_has_job(async_client):
    start()
    assert scheduler.get_job("auto_article") is not None
