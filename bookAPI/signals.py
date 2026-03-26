from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .cache_utils import bump_cache_version
from .models import Book, BookCategory


@receiver(post_save, sender=Book)
@receiver(post_delete, sender=Book)
@receiver(post_save, sender=BookCategory)
@receiver(post_delete, sender=BookCategory)
def invalidate_book_list_cache(**kwargs):
    bump_cache_version()
