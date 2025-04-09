from django.urls import path
from . import views
from .views import right_now

urlpatterns = [
    path("", views.index, name="index"),
    path("datetime/", right_now, name="right_now"),
]
