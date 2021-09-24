from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.entry, name="entry"),
    path("newArticle", views.newArticle, name="newArticle"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("search", views.search, name="search"),
    path("delete/<str:title>", views.delete, name="delete"),
    path("random_page", views.random_page, name="random")
]
