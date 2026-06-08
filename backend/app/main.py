from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from . import models
from .database import init_db
from .config import settings
from .routes import (
    auth_routes,
    ticket_routes,
    admin_routes,
    translation_routes
)

# Create database tables
init_db()

app = FastAPI(
    title=settings.APP_NAME,
    description="Enterprise SaaS for multilingual support ticket management",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload folder
uploads_path = Path(settings.UPLOAD_DIR)
uploads_path.mkdir(exist_ok=True)

app.mount(
    "/uploads",
    StaticFiles(directory=str(uploads_path)),
    name="uploads"
)

# Routers
app.include_router(auth_routes.router)
app.include_router(ticket_routes.router)
app.include_router(admin_routes.router)
app.include_router(translation_routes.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Multilingual Ticket Translator API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }