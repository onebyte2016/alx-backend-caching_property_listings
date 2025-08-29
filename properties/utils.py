from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection

def get_all_properties():
    # Try to get from cache
    all_properties = cache.get('all_properties')
    
    if all_properties is None:
        # If not cached, fetch from DB
        all_properties = Property.objects.all()
        # Store in cache for 1 hour (3600 seconds)
        cache.set('all_properties', all_properties, 3600)
    
    return all_properties


def get_redis_cache_metrics():
    """Retrieve Redis cache hit/miss metrics and calculate hit ratio."""
    conn = get_redis_connection("default")
    info = conn.info()

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    total = hits + misses

    hit_ratio = (hits / total) if total > 0 else 0.0

    metrics = {
        "hits": hits,
        "misses": misses,
        "hit_ratio": round(hit_ratio, 2),
    }

    # Log / Debug (you could also use logging)
    print(f"📊 Redis Metrics → Hits: {hits}, Misses: {misses}, Hit Ratio: {metrics['hit_ratio']}")

    return metrics

