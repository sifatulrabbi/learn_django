from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_handler, name="login"),
    path("logout/", views.logout_handler, name="logout"),
    path("register/", views.register_handler, name="register"),
    path("", views.home_handler, name="home"),
    path("room/<str:id>", views.room_handler, name="room"),
    path("create-room/", views.create_room_handler, name="create-room"),
    path("update-room/<str:id>", views.update_room_handler, name="update-room"),
    path("delete-room/<str:id>", views.delete_room_handler, name="delete-room"),
]
