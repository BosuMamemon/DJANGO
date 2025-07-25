from django.urls import path
from . import views

app_name = "test_app"
urlpatterns = [
    path('create/', views.create_post, name='create'),
    path('<int:post_id>/', views.get_post, name='read'),
    path('<int:post_id>/update/', views.update_post, name='update'),
    path('<int:post_id>/delete', views.delete_post, name='delete'),
    path('', views.get_posts, name='list'),
    path('<int:post_id>/download/', views.download_file, name='download'),
    path("imageTest/",views.image_test),
    path("create2/", views.create_post2, name='create2'),
]