from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.text import slugify
from .models import Post, Category, Tag

# Create your views here.

def index(request):
    return render(request, 'index.html')

def create_post(request):
    return render(request, "create-post.html")





class PostListView(View):
    """
    Display a list of published blog posts.
    """

    template_name = "posts/post_list.html"

    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(status=Post.Status.PUBLISHED).select_related("author", "category").prefetch_related("tags")
        return render(request, self.template_name, {"posts": posts})


class PostDetailView(View):
    """
    Display details of a single post.
    """

    template_name = "posts/post_detail.html"

    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLISHED)

        # Increment view counter
        post.increment_views()

        return render(request, self.template_name, {"post": post})


class PostCreateView(LoginRequiredMixin, View):
    """
    Allow authors to create a new blog post.
    """

    template_name = "posts/post_form.html"

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        tags = Tag.objects.all()
        return render(request, self.template_name, {"categories": categories, "tags": tags})

    def post(self, request, *args, **kwargs):
        user = request.user

        # Ensure user has an AuthorProfile
        if not hasattr(user, "authorprofile"):
            messages.error(request, "Only authors can create posts.")
            return redirect("post-list")

        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        status = request.POST.get("status", Post.Status.DRAFT)
        category_id = request.POST.get("category")
        tag_ids = request.POST.getlist("tags")

        # Basic validation
        if not title or not content:
            messages.error(request, "Title and content cannot be empty.")
            return redirect("post-create")

        category = Category.objects.filter(id=category_id).first()
        cover_image = request.FILES.get("cover_image")

        post = Post.objects.create(
            author=user.authorprofile,
            title=title,
            slug=slugify(title),
            content=content,
            category=category,
            cover_image=cover_image,
            status=status,
        )

        if tag_ids:
            post.tags.set(tag_ids)

        messages.success(request, "Post created successfully.")
        return redirect("post-detail", slug=post.slug)


class PostUpdateView(LoginRequiredMixin, View):
    """
    Allow authors to edit their own posts.
    """

    template_name = "posts/post_form.html"

    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)

        # Only author can edit
        if post.author.user != request.user:
            messages.error(request, "You are not authorized to edit this post.")
            return redirect("post-list")

        categories = Category.objects.all()
        tags = Tag.objects.all()

        return render(request, self.template_name, {"post": post, "categories": categories, "tags": tags})

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)

        if post.author.user != request.user:
            messages.error(request, "You are not authorized to edit this post.")
            return redirect("post-list")

        post.title = request.POST.get("title", "").strip()
        post.content = request.POST.get("content", "").strip()
        post.status = request.POST.get("status", Post.Status.DRAFT)
        post.category_id = request.POST.get("category") or None

        cover_image = request.FILES.get("cover_image")
        if cover_image:
            post.cover_image = cover_image

        tag_ids = request.POST.getlist("tags")
        post.save()
        post.tags.set(tag_ids)

        messages.success(request, "Post updated successfully.")
        return redirect("post-detail", slug=post.slug)


class PostDeleteView(LoginRequiredMixin, View):
    """
    Allow authors to delete their own posts.
    """

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)

        if post.author.user != request.user:
            messages.error(request, "You are not authorized to delete this post.")
            return redirect("post-list")

        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect("post-list")
