from fastapi import HTTPException, Request, Depends
from typing import Callable, Optional
import time
from app.core.redis import redis_client

class RateLimiter:
    def __init__(self, requests: int, window: int, key_func: Optional[Callable[[Request], str]] = None):
        self.requests = requests
        self.window = window # in seconds
        self.key_func = key_func

    async def __call__(self, request: Request):
        # Determine Key
        if self.key_func:
            identifier = self.key_func(request)
        else:
            # Default to IP
            identifier = request.client.host if request.client else "unknown"
            
        # Composite Redis Key: rate_limit:{path}:{identifier}
        # e.g. rate_limit:/api/v1/otp/generate:1.2.3.4
        key = f"rate_limit:{request.url.path}:{identifier}"
        
        # Simple Fixed Window
        # This implementation resets counter when key expires. 
        # For strict windows, we might use current time bucket.
        # Let's use INCR + EXPIRE (Token Bucket / Leaky Bucket approx)
        
        current = await redis_client.incr(key)
        if current == 1:
            await redis_client.expire(key, self.window)
            
        if current > self.requests:
            raise HTTPException(status_code=429, detail="Too Many Requests")

# Helpers for keys
def get_ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"

def get_user_id(request: Request) -> str:
    # Requires Auth middleware to have run or parsing payload manually if not dependable
    # For simplicity in this stack, getting IP is safer as default for unauth endpoints
    return request.client.host if request.client else "unknown"
