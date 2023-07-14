from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostDeleteView,
    UserPostListView,
    ReactView,
    GuestReactView,
    GuestPostCreateView,
    GuestPostDetailView
    )

urlpatterns = [
    path('',PostListView.as_view(), name='post-list'),
    path('post/react/<uuid:pk>/',ReactView.as_view(), name='post-reacts'),
    path('guest/post/react/<uuid:pk>/',GuestReactView.as_view(), name='guest-post-reacts'),
    path('user/<str:username>/',UserPostListView.as_view(), name='user-posts'),
    path('post/<uuid:pk>/',PostDetailView.as_view(), name='post-detail'),
    path('guest/post/<uuid:pk>/',GuestPostDetailView.as_view(), name='guest-post-detail'),
    path('post/new/',PostCreateView.as_view(), name='post-create'),
    path('guest/post/new/',GuestPostCreateView.as_view(), name='guest-post-create'),
    path('post/<uuid:pk>/delete/',PostDeleteView.as_view(), name='post-delete'),
]

