from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings
from backend.core.database import init_db
from backend.routes import auth

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="MediFederate Backend API — Real authentication + Medical features",
)

# CORS (allow Streamlit, HTML website, mobile apps)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """Create database tables on startup."""
    init_db()
    print(f"✅ {settings.APP_NAME} v{settings.APP_VERSION} started")


# ========================================
# ROUTERS
# ========================================
app.include_router(auth.router)


# ========================================
# HEALTH CHECK
# ========================================
@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "status": "Active",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}