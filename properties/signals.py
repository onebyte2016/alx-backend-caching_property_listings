from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property


@receiver(post_save, sender=Property)
def clear_cache_on_save(sender, instance, **kwargs):
    """Clear cached properties whenever a Property is created or updated."""
    cache.delete('all_properties')
    print("🚀 Redis cache 'all_properties' invalidated after SAVE/UPDATE.")


@receiver(post_delete, sender=Property)
def clear_cache_on_delete(sender, instance, **kwargs):
    """Clear cached properties whenever a Property is deleted."""
    cache.delete('all_properties')
    print("🗑️ Redis cache 'all_properties' invalidated after DELETE.")
