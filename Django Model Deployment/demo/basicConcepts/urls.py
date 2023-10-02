from django.urls import path
from . import views

urlpatterns = [
    path("ashioya", views.Welcome)
]


# You can change the route of the URL by changing the path in the urlpatterns list.