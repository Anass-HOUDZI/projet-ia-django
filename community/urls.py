from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('api/posts/', views.api_posts, name='api_posts'),
    path('api/posts/<int:post_id>/like/', views.api_like_post, name='api_like_post'),
    path('api/posts/<int:post_id>/reply/', views.api_add_reply, name='api_add_reply'),
]
