from django.urls import path

from . import views

urlpatterns = [
    path("", views.home),
    path("insert_form/", views.insert_form),
    path("insert/", views.insert),
    path("board_list/", views.board_list),
    path("board_page/", views.board_page),
    path("detail/", views.detail),
    path('download_count/', views.download_count),
    path('download/', views.download),
    path('delete/<int:id>/', views.delete),
    path('update_form/<int:id>/', views.update_form),
    path('update/<int:id>/', views.update),
    path('comment_insert/<int:id>/', views.comment_insert),
    path('sign_up/', views.sign_up)
]