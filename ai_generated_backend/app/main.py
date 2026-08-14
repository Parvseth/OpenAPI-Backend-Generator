from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import engine, Base

from app.api import customer_router

from app.api import customercreate_router

from app.api import customerstatus_router

from app.api import product_router

from app.api import ordercreate_router

from app.api import orderitem_router


# Create Database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Healthcheck Endpoint
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME, "version": settings.VERSION}

# Register API Routers

app.include_router(customer_router.router, prefix=settings.API_V1_STR)

app.include_router(customercreate_router.router, prefix=settings.API_V1_STR)

app.include_router(customerstatus_router.router, prefix=settings.API_V1_STR)

app.include_router(product_router.router, prefix=settings.API_V1_STR)

app.include_router(ordercreate_router.router, prefix=settings.API_V1_STR)

app.include_router(orderitem_router.router, prefix=settings.API_V1_STR)
