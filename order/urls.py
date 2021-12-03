from django.urls import path

from order import views

urlpatterns = [
    path("shops/", views.shop),
    path("menus/", views.menu),
]
