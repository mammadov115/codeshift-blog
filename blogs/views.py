from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.text import slugify
from .models import Post, Category, Tag, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .utils import search_posts


# Create your views here.


class AllPostsView(View):
    """
    Display a paginated list of published blog posts.
    """

    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        # Fetch all posts with related data for efficiency
        posts_queryset = (
            Post.objects.all()
            .select_related("author", "category")
            .prefetch_related("tags")
        )

        search_query = request.GET.get("query", "").strip()
        category_id = request.GET.get("category")

        if category_id:
            posts_queryset = posts_queryset.filter(category__id=category_id)

        # Apply search filter if a query is present
        if search_query:
            posts_queryset = search_posts(search_query)

        # Set up pagination
        page = request.GET.get("page", 1)
        paginator = Paginator(posts_queryset, 5)  # 5 posts per page

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g., 9999), deliver last page.
            posts = paginator.page(paginator.num_pages)

        context = {
            "posts": posts,
            "search_query": search_query,
        }

        return render(request, self.template_name, context)


class PostListView(View):
    """
    Display a list of published blog posts.
    """

    template_name = "post-list.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        author_profile = getattr(user, "authorprofile", None)
        posts = Post.objects.filter(author=author_profile).select_related("author", "category").prefetch_related("tags")
        return render(request, self.template_name, {"posts": posts})


class PostDetailView(View):
    """
    Display details of a single post.
    """

    template_name = "post.html"

    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLISHED)
        categories = Category.objects.all()
        related_posts = Post.objects.filter(category=post.category).exclude(id=post.id).distinct()[:4]

        search_query = request.GET.get("query", "").strip()
        if search_query:
            return redirect(f"/?query={search_query}")


        # Increment view counter
        post.increment_views()

        return render(request, self.template_name, {"post": post, "categories": categories, "related_posts":related_posts})
    
    def post(self, request, slug, *args, **kwargs):
        """Handle new comment submissions."""
        post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLISHED)
        categories = Category.objects.all()

        content = request.POST.get("message", "").strip()
        parent_id = request.POST.get("parent_id")  # for reply comments

        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to comment.")
            return redirect("login")  # Adjust your login URL name if different

        if content:
            parent_comment = Comment.objects.filter(id=parent_id).first() if parent_id else None

            Comment.objects.create(
                post=post,
                user=request.user,
                content=content,
                parent=parent_comment
            )
            messages.success(request, "Your comment was added successfully!")
        else:
            messages.warning(request, "Comment cannot be empty.")

        return redirect("post-detail", slug=slug)


class PostCreateView(LoginRequiredMixin, View):
    """
    Allow authors to create a new blog post.
    """

    template_name = "post-create.html"

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        tags = Tag.objects.all()
        return render(request, self.template_name, {"categories": categories, "tags": tags})

    def post(self, request, *args, **kwargs):
        user = request.user

        # Ensure user has an AuthorProfile
        if not hasattr(user, "authorprofile"):
            return redirect("post-list")

        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        status = request.POST.get("status", Post.Status.DRAFT)
        category_id = request.POST.get("category")

        cover_image = request.FILES.get("cover_image")
        
        # Basic validation
        if not title or not content:
            return redirect("post-create")

        category = Category.objects.filter(name=category_id).first()

        post = Post.objects.create(
            author=user.authorprofile,
            title=title,
            slug=slugify(title),
            content=content,
            category=category,
            cover_image=cover_image,
            status=status,
        )



        return redirect("post-list")


class PostUpdateView(LoginRequiredMixin, View):
    """
    Allow authors to edit their own posts.
    """

    template_name = "post-edit.html"

    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)

        # Only author can edit
        if post.author.user != request.user:
            return redirect("post-list")

        categories = Category.objects.all()
        tags = Tag.objects.all()

        return render(request, self.template_name, {"post": post, "categories": categories, "tags": tags})

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)

        if post.author.user != request.user:
            return redirect("post-list")

        post.title = request.POST.get("title", "").strip()
        post.content = request.POST.get("content", "").strip()
        post.status = request.POST.get("status", Post.Status.DRAFT)
        category_name = request.POST.get("category") or None
        category = Category.objects.filter(name=category_name).first()
        post.category = category

        cover_image = request.FILES.get("cover_image")
        if cover_image:
            post.cover_image = cover_image

        tag_ids = request.POST.getlist("tags")
        post.save()
        post.tags.set(tag_ids)

        return redirect("post-update", slug=post.slug)


class PostDeleteView(LoginRequiredMixin, View):
    """
    Allow authors to delete their own posts.
    """

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)

        if post.author.user != request.user:
            return redirect("post-list")

        post.delete()
        return redirect("post-list")