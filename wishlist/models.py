from django.conf import settings
from django.db import models


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wishlists")
    person_name = models.CharField(max_length=120)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "-created_at"]

    def __str__(self):
        return f"{self.title} ({self.person_name})"


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name="items")
    description = models.CharField(max_length=300)
    url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    is_purchased = models.BooleanField(default=False)
    priority = models.PositiveSmallIntegerField(default=3)  # 1=High, 2=Med, 3=Low by default
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["is_purchased", "priority", "-created_at"]

    def __str__(self):
        return f"{self.description} (prio {self.priority})"