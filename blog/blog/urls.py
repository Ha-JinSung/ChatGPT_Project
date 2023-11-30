from django.urls import path
from . import views


app_name = 'blog'


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('new/', views.post_new, name='post_new'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('<int:pk>/comment/new/', views.comment_new, name='comment_new'),
    path('<int:post_pk>/comment/<int:comment_pk>/edit/', views.comment_edit, name='comment_edit'),
    path('<int:post_pk>/comment/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:post_pk>/comment/<int:comment_pk>/reply/', views.comment_reply, name='comment_reply'),
    path('<int:post_pk>/comment/<int:comment_pk>/reply/<int:reply_pk>/edit/', views.reply_edit, name='reply_edit'),
    path('<int:post_pk>/comment/<int:comment_pk>/reply/<int:reply_pk>/delete/', views.reply_delete, name='reply_delete'),
]


