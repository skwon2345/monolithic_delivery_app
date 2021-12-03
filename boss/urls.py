from django.urls import path

from boss import views

urlpatterns = [
    path("timeinput/", views.time_input, name="timeinput"),
]
