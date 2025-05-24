from typing import Any

from django.views.generic import DetailView
from django.views.generic.base import TemplateView

from .models import Category, Post


class PostListView(TemplateView):
    template_name = "posts_list.html"
    extra_context = {"title": "Все записи"}

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if "category" in self.request.GET:
            category = Category.objects.get(slug=self.request.GET["category"])
            context["category"] = category
            context["posts"] = category.posts.filter(is_published=True)
            context["title"] = category.name

        if "category" not in context:
            context["posts"] = Post.objects.filter(is_published=True)[:3]
            context["categories"] = Category.objects.all()
        return context


class PostDetailView(DetailView[Post]):
    model = Post
    template_name = "posts_detail.html"
