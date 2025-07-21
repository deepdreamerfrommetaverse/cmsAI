import logging, contextlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.scheduler import start as sched_start, shutdown as sched_shutdown

logging.basicConfig(level=logging.INFO)

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    sched_start()
    yield
    # Shutdown
    await sched_shutdown()

app = FastAPI(title="AI CMS Enterprise", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"status": "ok"}
