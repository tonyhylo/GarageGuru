from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('messages/', views.messages, name='messages'),
    path('profile/', views.profile, name='profile'),
    path('posts/<int:post_id>/', views.posts_detail, name='detail'),
    path('posts/', views.post_index, name='index'),
    path('posts/create/', views.PostCreate.as_view(), name='posts_create'),
    path('posts/<int:pk>/update/', views.PostUpdate.as_view(), name='posts_update'),
    path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name='posts_delete'),
    path('posts/<int:post_id>/add_photo/', views.add_photo, name='add_photo'),
    # path('posts/<int:post_id>/delete_photo/', views.delete_photo, name='delete_photo'),
    path('posts/<int:post_id>/delete_photo/<int:photo_id>', views.delete_photo, name='delete_photo'),
    path('posts/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    path('posts/<int:post_id>/commentDelete/<int:comment_id>', views.delete_comment, name='comment_delete'),
    path('accounts/signup/', views.signup, name='signup'),
]
