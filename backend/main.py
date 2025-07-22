# backend/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

# Import project modules
import models
from database import engine
from routers import auth, analysis
from limiter import limiter

# Create all database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Resume Scanner API",
    version="1.0.0"
)

# --- Add CORS Middleware (NEW) ---
# This allows our frontend (running on localhost:3000) to communicate with our backend.
origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all HTTP methods
    allow_headers=["*"], # Allow all HTTP headers
)
# --------------------------------

# --- Add Rate Limiting Middleware ---
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda request, exc: _rate_limit_exceeded_handler(request, exc))
# Note: A lambda is used here to match the expected function signature.
# ------------------------------------

# Include the routers from the 'routers' directory
app.include_router(auth.router)
app.include_router(analysis.router)

@app.get("/", tags=["Health Check"])
@limiter.limit("100/minute") # Also rate limit the health check
async def root(request: Request):
    return {"status": "ok", "message": "API is running!"}