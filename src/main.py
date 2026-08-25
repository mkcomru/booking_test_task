from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.modules.booking.routers import router as booking_router
from src.modules.core.database import engine
from src.modules.core.handlers import register_exception_handlers
from src.modules.core.logging_setup import setup_logging
from src.modules.core.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    setup_logging(environment=settings.environment, debug=settings.debug)

    yield

    await engine.dispose()


app = FastAPI(title="Booking API", lifespan=lifespan)

register_exception_handlers(app)
app.include_router(booking_router)
