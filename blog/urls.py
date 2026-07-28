from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.blog_list,
        name="blog_list"
    ),


    path(
        "create/",
        views.blog_create,
        name="blog_create"
    ),


    path(
        "dashboard/",
        views.author_dashboard,
        name="author_dashboard"
    ),


    path(
        "<slug:slug>/like/",
        views.like_blog,
        name="like_blog"
    ),


    path(
        "<slug:slug>/update/",
        views.blog_update,
        name="blog_update"
    ),


    path(
        "<slug:slug>/delete/",
        views.blog_delete,
        name="blog_delete"
    ),


    path(
        "<slug:slug>/",
        views.blog_detail,
        name="blog_detail"
    ),


    path(
        "author/<str:username>/",
        views.author_profile,
        name="author_profile"
    ),

]