from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin[Post]):
    list_display = ("title", "status", "created_at")
    list_filter = ("status", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "body")
    date_hierarchy = "created_at"
