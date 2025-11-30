from django.contrib import admin
from .models import Wishlist, WishlistItem

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "person_name", "user", "updated_at", "created_at")
    list_filter = ("updated_at", "created_at")
    search_fields = ("title", "person_name", "user__username", "user__email")

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ("id", "wishlist", "description", "priority", "is_purchased", "created_at")
    list_filter = ("is_purchased", "priority", "created_at")
    search_fields = ("description", "wishlist__title", "wishlist__person_name")