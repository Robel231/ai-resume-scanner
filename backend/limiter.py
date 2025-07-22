# backend/limiter.py

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
import redis
import os

from security import get_current_user

# --- PRODUCTION-AWARE REDIS URL ---
# Deployment platforms like Render provide a single REDIS_URL.
REDIS_URL = os.getenv("REDIS_URL")

# If REDIS_URL is not found, we fall back to our local Docker service name.
if not REDIS_URL:
    print("REDIS_URL not found, falling back to local Docker service 'redis'...")
    REDIS_URL = "redis://redis:6379"

# --- Redis Connection ---
try:
    # Attempt to connect to the Redis instance
    redis_instance = redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
    # Ping the server to check the connection
    redis_instance.ping()
    print("Successfully connected to Redis.")
except redis.exceptions.ConnectionError as e:
    print(f"Could not connect to Redis: {e}. Rate limiting will use in-memory storage.")
    redis_instance = None


# --- Key Function ---
# This function tells the rate limiter HOW to identify a user.
def key_func(request: Request) -> str:
    # If the user is authenticated, their info is attached to the request scope by our dependency.
    # We use this to rate-limit on a per-user basis.
    if hasattr(request.state, 'user') and request.state.user:
        return str(request.state.user.id)
    
    # Fallback to the user's IP address if they are not authenticated.
    return get_remote_address(request)


# --- Create the Limiter Instance ---
# Use the REDIS_URL for storage. If the connection failed, it gracefully falls back to memory.
limiter = Limiter(
    key_func=key_func,
    storage_uri=REDIS_URL if redis_instance else "memory://",
    strategy="fixed-window"
)