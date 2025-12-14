"""Cache service for query results."""
import json
import hashlib
from typing import Optional, Any, Dict
import redis
from config.settings import settings


class CacheService:
    """Redis-based cache service."""
    
    def __init__(self):
        """Initialize cache service."""
        self.enabled = settings.ENABLE_CACHE
        self.ttl = settings.CACHE_TTL
        self.redis_client = None
        
        if self.enabled:
            try:
                self.redis_client = redis.Redis(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=settings.REDIS_DB,
                    password=settings.REDIS_PASSWORD,
                    decode_responses=True,
                )
                # Test connection
                self.redis_client.ping()
            except Exception as e:
                print(f"Warning: Redis connection failed: {e}. Caching disabled.")
                self.enabled = False
                self.redis_client = None
    
    def _generate_cache_key(self, query_dict: Dict[str, Any]) -> str:
        """Generate a cache key from query parameters."""
        # Sort and serialize for consistent hashing
        query_str = json.dumps(query_dict, sort_keys=True)
        return f"query:{hashlib.sha256(query_str.encode()).hexdigest()}"
    
    def get(self, query_dict: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get cached query result."""
        if not self.enabled or not self.redis_client:
            return None
        
        try:
            cache_key = self._generate_cache_key(query_dict)
            cached_data = self.redis_client.get(cache_key)
            
            if cached_data:
                return json.loads(cached_data)
            return None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None
    
    def set(self, query_dict: Dict[str, Any], result: Dict[str, Any], ttl: Optional[int] = None) -> bool:
        """Cache query result."""
        if not self.enabled or not self.redis_client:
            return False
        
        try:
            cache_key = self._generate_cache_key(query_dict)
            cache_ttl = ttl or self.ttl
            
            self.redis_client.setex(
                cache_key,
                cache_ttl,
                json.dumps(result)
            )
            return True
        except Exception as e:
            print(f"Cache set error: {e}")
            return False
    
    def invalidate(self, pattern: str = "*") -> int:
        """Invalidate cache entries matching pattern."""
        if not self.enabled or not self.redis_client:
            return 0
        
        try:
            keys = self.redis_client.keys(f"query:{pattern}")
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except Exception as e:
            print(f"Cache invalidate error: {e}")
            return 0
    
    def is_connected(self) -> bool:
        """Check if cache is connected."""
        if not self.enabled or not self.redis_client:
            return False
        
        try:
            self.redis_client.ping()
            return True
        except:
            return False
    
    def close(self):
        """Close cache connection."""
        if self.redis_client:
            self.redis_client.close()


# Global cache service instance
cache_service = CacheService()
