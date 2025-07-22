

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware


import models
from database import engine
from routers import auth, analysis
from limiter import limiter


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Resume Scanner API",
    version="1.0.0"
)



origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)



app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda request, exc: _rate_limit_exceeded_handler(request, exc))




app.include_router(auth.router)
app.include_router(analysis.router)

@app.get("/", tags=["Health Check"])
@limiter.limit("100/minute") 
async def root(request: Request):
    return {"status": "ok", "message": "API is running!"}