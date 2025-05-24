from django.contrib import admin

from .models import Category, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin[Post]):
    list_display = ("title", "is_published", "created_at")
    list_filter = ("is_published", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "body")
    date_hierarchy = "created_at"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin[Category]):
    list_display = ("name",)
    list_filter = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
