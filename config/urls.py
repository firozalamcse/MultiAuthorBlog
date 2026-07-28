"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from blog import views

urlpatterns = [
    path("", views.home, name="home"),
    path("admin/", admin.site.urls),

    # Accounts App
    path("accounts/", include("accounts.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )