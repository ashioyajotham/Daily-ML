from django.urls import path
from . import views

urlpatterns = [
    path("", views.Welcome, name="Welcome"),
    path("user", views.User, name="User")
]


# You can change the route of the URL by changing the path in the urlpatterns list.