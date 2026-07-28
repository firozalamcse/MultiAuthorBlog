from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Sum, Q
from django.core.paginator import Paginator

from .models import Blog, Category, Tag, Comment
from .forms import BlogForm, CommentForm


# Home Page
def home(request):
    return render(request, "home.html")


# Blog List
def blog_list(request):

    query = request.GET.get("q", "")
    category = request.GET.get("category", "")
    tag = request.GET.get("tag", "")

    blogs = Blog.objects.filter(status="published")

    if category:
        blogs = blogs.filter(category_id=category)

    if tag:
        blogs = blogs.filter(tags__id=tag)

    if query:
        blogs = blogs.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    blogs = blogs.order_by("-created_at")

    paginator = Paginator(blogs, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "blogs": page_obj,
        "page_obj": page_obj,
        "query": query,
        "categories": Category.objects.all(),
        "tags": Tag.objects.all(),
        "selected_category": category,
        "selected_tag": tag,
    }

    return render(
        request,
        "blog/blog_list.html",
        context
    )


# Blog Detail + Comments
def blog_detail(request, slug):

    blog = get_object_or_404(
        Blog,
        slug=slug,
        status="published"
    )

    # Increase View Count
    blog.view_count += 1
    blog.save(update_fields=["view_count"])

    # Save Comment
    if request.method == "POST":

        if request.user.is_authenticated:

            form = CommentForm(request.POST)

            if form.is_valid():

                comment = form.save(commit=False)
                comment.blog = blog
                comment.user = request.user
                comment.save()

                return redirect(
                    "blog_detail",
                    slug=blog.slug
                )

        else:
            return redirect("login")

    else:
        form = CommentForm()

    comments = blog.comments.all()

    context = {
        "blog": blog,
        "form": form,
        "comments": comments,
        "liked": (
            request.user.is_authenticated and
            blog.likes.filter(id=request.user.id).exists()
        ),
    }

    return render(
        request,
        "blog/blog_detail.html",
        context
    )


# Like / Unlike Blog
@login_required
def like_blog(request, slug):

    blog = get_object_or_404(
        Blog,
        slug=slug,
        status="published"
    )

    if blog.likes.filter(id=request.user.id).exists():

        blog.likes.remove(request.user)

    else:

        blog.likes.add(request.user)

    return redirect(
        "blog_detail",
        slug=slug
    )


# Create Blog
@login_required
def blog_create(request):

    if request.method == "POST":

        form = BlogForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            form.save_m2m()

            return redirect(
                "blog_detail",
                slug=blog.slug
            )

    else:
        form = BlogForm()

    return render(
        request,
        "blog/blog_create.html",
        {
            "form": form
        }
    )


# Update Blog
@login_required
def blog_update(request, slug):

    blog = get_object_or_404(
        Blog,
        slug=slug
    )

    if blog.author != request.user:
        return HttpResponseForbidden(
            "You are not allowed to edit this post."
        )

    if request.method == "POST":

        form = BlogForm(
            request.POST,
            request.FILES,
            instance=blog
        )

        if form.is_valid():

            form.save()

            return redirect(
                "blog_detail",
                slug=blog.slug
            )

    else:

        form = BlogForm(
            instance=blog
        )

    return render(
        request,
        "blog/blog_update.html",
        {
            "form": form,
            "blog": blog
        }
    )


# Delete Blog
@login_required
def blog_delete(request, slug):

    blog = get_object_or_404(
        Blog,
        slug=slug
    )

    if blog.author != request.user:
        return HttpResponseForbidden(
            "You are not allowed to delete this post."
        )

    if request.method == "POST":
        blog.delete()
        return redirect("blog_list")

    return render(
        request,
        "blog/blog_confirm_delete.html",
        {
            "blog": blog
        }
    )


# Author Dashboard
@login_required
def author_dashboard(request):

    posts = Blog.objects.filter(
        author=request.user
    ).order_by("-created_at")

    context = {
        "total_posts": posts.count(),
        "published_posts": posts.filter(status="published").count(),
        "draft_posts": posts.filter(status="draft").count(),
        "total_views": posts.aggregate(
            total=Sum("view_count")
        )["total"] or 0,
        "recent_posts": posts[:5],
    }

    return render(
        request,
        "blog/author_dashboard.html",
        context
    )

# Public Author Profile
def author_profile(request, username):

    from django.contrib.auth import get_user_model

    User = get_user_model()

    author = get_object_or_404(
        User,
        username=username
    )

    posts = Blog.objects.filter(
        author=author,
        status="published"
    )

    context = {

        "author": author,

        "posts": posts,

        "total_posts": posts.count(),

        "total_views": posts.aggregate(
            total=Sum("view_count")
        )["total"] or 0,

        "total_likes": sum(
            post.likes.count()
            for post in posts
        ),

    }


    return render(
        request,
        "blog/author_profile.html",
        context
    )