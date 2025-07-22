# backend/limiter.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Create a limiter instance. `get_remote_address` is the default key function.
# We will override this to use the current user's email.
limiter = Limiter(key_func=get_remote_address)