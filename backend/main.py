"""
AI CMS Enterprise · Main entry‑point (FastAPI)

• zachowuje 100 % Twojej logiki (CORS, routery, Stripe init, run_scheduler)
• dodaje:
    – root redirect → /docs,
    – dodatkowy start_article_scheduler (świeży artykuł co N h),
    – router /social (X & Instagram), chroniony admin‑JWT.
"""

import logging
import asyncio
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from core.settings import settings
from core.auth import get_current_admin
from database import get_db, SessionLocal, engine  # noqa: F401  (future use)
from fastapi.staticfiles import StaticFiles
from pathlib import Path


# === istniejące routery ===
from routers import (
    auth as auth_router,
    users as users_router,
    articles as articles_router,
    feedback as feedback_router,
    analytics as analytics_router,
    stripe as stripe_router,
)

# === nowy router Social ===
from routers import social as social_router  # plik dodany poniżej

# === scheduler ===
from scheduler import (
    run_scheduler,             # Twój oryginalny publikator
    start_article_scheduler,   # nowy – generator artykułów
    stop_scheduler,            # hook zamknięcia
)

# --------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI CMS Enterprise Backend",
    description="Automated CMS: OpenAI, WordPress+Bricks, DALL·E, Stripe, X, Instagram",
    version="1.1.0",
)



# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- / root → /docs ----------
@app.get("/", include_in_schema=False)
def root(_: Request):
    """Convenience redirect to the interactive docs."""
    return RedirectResponse(url="/docs")

# ---------- STARTUP ----------
@app.on_event("startup")
async def startup_event():
    if settings.stripe_api_key:
        import stripe
        stripe.api_key = settings.stripe_api_key
        logger.info("Stripe API key configured.")

    if settings.wordpress_url and settings.wordpress_username and settings.wordpress_password:
        logger.info("Launching schedulers (publish & generate)…")
        # 1) Twój harmonogram publikacji
        app.state.publish_task = asyncio.create_task(run_scheduler())
        # 2) nowy harmonogram generujący artykuły
        app.state.generate_task = asyncio.create_task(start_article_scheduler(app))
    else:
        logger.warning("WordPress not configured – schedulers skipped.")

# ---------- SHUTDOWN ----------
@app.on_event("shutdown")
async def shutdown_event():
    """Cancel background tasks and run custom stop‑hook."""
    async def _cancel(name: str):
        task = getattr(app.state, name, None)
        if task:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                logger.info("Task %s cancelled.", name)

    await _cancel("publish_task")
    await _cancel("generate_task")
    await stop_scheduler()

# ---------- API routery ----------
API = "/api"

app.include_router(auth_router.router,     prefix=f"{API}/auth",     tags=["Auth"])
app.include_router(users_router.router,    prefix=f"{API}/users",    tags=["Users"], dependencies=[Depends(get_current_admin)])
app.include_router(articles_router.router, prefix=f"{API}/articles", tags=["Articles"])
app.include_router(feedback_router.router, prefix=f"{API}/feedback", tags=["Feedback"])
app.include_router(analytics_router.router,prefix=f"{API}/analytics",tags=["Analytics"])
app.include_router(stripe_router.router,   prefix=f"{API}/stripe",   tags=["Stripe"], dependencies=[Depends(get_current_admin)])
app.include_router(social_router.router,   prefix=f"{API}/social",   tags=["Social"], dependencies=[Depends(get_current_admin)])


# 1) katalog (ten sam, do którego zapisujesz obrazki)
STATIC_ROOT = Path("static")
STATIC_ROOT.mkdir(exist_ok=True)

# 2) montujemy pod /static  →  http://backend:8000/static/…
app.mount(
    "/static",
    StaticFiles(directory=STATIC_ROOT, html=False),  # html=False - nie podawaj index.html
    name="static",
)


# ---------- Lokalne uruchomienie ----------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
