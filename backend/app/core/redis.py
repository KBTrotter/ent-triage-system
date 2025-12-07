"""Redis client configuration.

Redis is used for storing authentication refresh tokens and for
caching AI triage results.  This module exposes a single shared
client instance which connects to the Redis server specified by
``REDIS_URL`` in :mod:`app.core.config`.  The client is safe to
reuse across requests because it maintains its own connection pool.
"""

import redis  # type: ignore

from app.core.config import settings


# Create a Redis client from the configured URL.  The returned
# instance will lazily connect to Redis on first use and will manage
# its own pool of connections.  See the redis-py documentation for
# additional configuration options.
redis_client = redis.Redis.from_url(settings.REDIS_URL)
