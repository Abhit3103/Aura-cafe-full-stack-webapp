
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import menu, cart, order, admin, auth




# Create database tables
models.Base.metadata.create_all(bind=engine)


def create_application() -> FastAPI:
    
    app = FastAPI(
        title="Aura Cafe API",
        description="Backend API for Aura Cafe ordering system",
        version="1.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )

    # C onfigure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # TODO: Restrict to specific origins in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
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


