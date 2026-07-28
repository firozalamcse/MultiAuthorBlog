from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from blog.models import Blog


User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "username",
        "email",
        "is_staff",
        "is_active",
        "date_joined",
        "total_blogs",
    )


    search_fields = (
        "username",
        "email",
    )


    list_filter = (
        "is_staff",
        "is_active",
        "date_joined",
    )


    def total_blogs(self, obj):

        return Blog.objects.filter(
            author=obj
        ).count()


    total_blogs.short_description = "Blogs"