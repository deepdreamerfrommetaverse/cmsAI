from fastapi import APIRouter
from app.api.v1.endpoints import auth, articles, analytics, feedback, social

api_router = APIRouter(prefix="/v1")
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(articles.router, prefix="/articles", tags=["articles"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
api_router.include_router(social.router, prefix="/social", tags=["social"])
