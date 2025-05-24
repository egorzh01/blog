from django.db import models
from django.db.models import QuerySet
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
    )
    image = models.ImageField(
        upload_to="category/",
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    @property
    def recent_posts(self) -> QuerySet["Post", "Post"]:
        return self.posts.all()[:3]


class Post(models.Model):
    title = models.CharField(
        max_length=128,
        unique=True,
    )
    slug = models.SlugField(
        max_length=128,
        unique=True,
    )
    body = models.TextField(
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    is_published = models.BooleanField(
        default=False,
    )
    categories = models.ManyToManyField(
        Category,
        related_name="posts",
    )
    image = models.ImageField(
        upload_to="category/",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("blog:post_detail", args=[self.slug])
