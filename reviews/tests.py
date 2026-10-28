
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.test import TestCase

from .models import Review


class ReviewCacheInvalidationTests(TestCase):

    def setUp(self):
        cache.clear()

    def tearDown(self):
        cache.clear()

    def test_review_save_invalidates_cache(self):
        cache.set("test:review-cache", "stale", timeout=300)

        post_save.send(
            sender=Review,
            instance=None,
            created=True,
            raw=False,
            using="default",
            update_fields=None,
        )

        self.assertIsNone(cache.get("test:review-cache"))

    def test_review_delete_invalidates_cache(self):
        cache.set("test:review-cache", "stale", timeout=300)

        post_delete.send(
            sender=Review,
            instance=None,
            using="default",
        )

        self.assertIsNone(cache.get("test:review-cache"))
