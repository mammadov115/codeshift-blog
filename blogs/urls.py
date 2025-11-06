from django.urls import path
from . import views

urlpatterns = [
    path('', views.AllPostsView.as_view(), name='home' ),
    path("post-list/", views.PostListView.as_view(), name="post-list"),
    path("create/", views.PostCreateView.as_view(), name="post-create"),
    path("<slug:slug>/", views.PostDetailView.as_view(), name="post-detail"),
    path("<slug:slug>/edit/", views.PostUpdateView.as_view(), name="post-update"),
    path("<slug:slug>/delete/", views.PostDeleteView.as_view(), name="post-delete"),
]
