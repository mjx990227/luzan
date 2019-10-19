from django.urls import path

from . import views
urlpatterns = [
    path("index/",views.index),
    path("detail/",views.detail),
    path("column/",views.column),
]