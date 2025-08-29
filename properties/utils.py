from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging


# def get_all_properties():
#     # Try to get from cache
#     all_properties = cache.get('all_properties')
    
#     if all_properties is None:
#         # If not cached, fetch from DB
#         all_properties = Property.objects.all()
#         # Store in cache for 1 hour (3600 seconds)
#         cache.set('all_properties', all_properties, 3600)
    
#     return all_properties

logger = logging.getLogger(__name__)

def get_all_properties():
    from django.core.cache import cache
    from .models import Property
    properties = cache.get('all_properties')
    if not properties:
        properties = list(Property.objects.all())
        cache.set('all_properties', properties, 3600)  # cache for 1 hour
    return properties

def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss metrics and calculate hit ratio.
    """
    try:
        conn = get_redis_connection("default")
        info = conn.info("stats")
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total_requests = hits + misses
        hit_ratio = hits / total_requests if total_requests > 0 else 0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": hit_ratio,
        }

        logger.info(f"Redis Cache Metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {e}")
        return {
            "hits": 0,
            "misses": 0,
            "hit_ratio": 0,
        }
    print(f"📊 Redis Metrics → Hits: {hits}, Misses: {misses}, Hit Ratio: {metrics['hit_ratio']}")

    return metrics


# def get_redis_cache_metrics():
#     """Retrieve Redis cache hit/miss metrics and calculate hit ratio."""
#     conn = get_redis_connection("default")
#     info = conn.info()

#     hits = info.get("keyspace_hits", 0)
#     misses = info.get("keyspace_misses", 0)
#     total = hits + misses

#     hit_ratio = (hits / total) if total > 0 else 0

#     metrics = {
#         "hits": hits,
#         "misses": misses,
#         "hit_ratio": round(hit_ratio, 2),
#     }

    # Log / Debug (you could also use logging)
    # print(f"📊 Redis Metrics → Hits: {hits}, Misses: {misses}, Hit Ratio: {metrics['hit_ratio']}")

    # return metrics
   






