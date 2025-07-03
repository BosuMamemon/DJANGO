from django.urls import path
from app01 import views

urlpatterns = [
    path("", views.list),
    path("write_form/", views.write_form, name="write"),
    path("write/", views.write),
    path("list/", views.list),
    path("detail_idx/", views.detail_idx),
    path("detail/<int:board_idx>/", views.detail),
    path("delete/<int:board_idx>/", views.delete),
    path("update_form/<int:board_idx>/", views.update_form),
    path("update/", views.update),
    path("download_count/", views.download_count),
    path("download/", views.download),
    #     Comment 관련
    path("comment_insert/", views.comment_insert),
]
