from django.contrib import admin

from .models import Blog, Category, Tag, Comment



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
    )

    search_fields = (
        "name",
    )



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = (
        "name",
    )

    search_fields = (
        "name",
    )



@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "author",
        "category",
        "status",
        "view_count",
        "created_at",
    )


    list_filter = (
        "status",
        "category",
        "created_at",
    )


    search_fields = (
        "title",
        "content",
        "author__username",
    )


    readonly_fields = (
        "slug",
        "view_count",
        "created_at",
        "updated_at",
    )



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = (
        "blog",
        "user",
        "created_at",
    )


    search_fields = (
        "blog__title",
        "user__username",
        "content",
    )


    list_filter = (
        "created_at",
    )