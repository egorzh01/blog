from django.views.generic import DetailView, ListView

from .models import Post


class PostListView(ListView[Post]):
    queryset = Post.objects.filter(status="published")
    paginate_by = 5
    context_object_name = "posts"
    template_name = "post_list.html"


class PostDetailView(DetailView[Post]):
    model = Post
    template_name = "post_detail.html"
