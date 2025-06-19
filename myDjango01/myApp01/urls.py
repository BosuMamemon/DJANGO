from django.urls import path
from myApp01 import views

urlpatterns = [
    path("", views.write_form),
    path("insert/", views.insert)
]