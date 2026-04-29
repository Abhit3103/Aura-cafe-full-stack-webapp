import logging
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import models
from database import engine
from routers import menu, cart, order, admin, auth

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# CORS origins: explicit production + local dev
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://aura-cafe-frontend.vercel.app")
ALLOWED_ORIGINS = [
    FRONTEND_URL,
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8080",
    "https://aura-cafe-full-stack-webapp-production.up.railway.app",
]


def create_application() -> FastAPI:
    app = FastAPI(
        title="Aura Cafe API",
        description="Backend API for Aura Cafe ordering system",
        version="1.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Global exception handler to ensure CORS headers are ALWAYS present,
    # even on 500 errors that bypass normal middleware flow.
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception: %s", exc)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error. Please try again later."},
        )

    # Register routers
    app.include_router(menu.router, prefix="/menu", tags=["Menu"])
    app.include_router(cart.router, prefix="/cart", tags=["Cart"])
    app.include_router(order.router, prefix="/orders", tags=["Orders"])
    app.include_router(auth.router, tags=["Authentication"])
    app.include_router(admin.router, tags=["Admin"])

    @app.get("/", tags=["Health"])
    def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "service": "Aura Cafe API"}

    return app


# Create the application instance
app = create_application()

