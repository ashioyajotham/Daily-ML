from django.urls import path
from . import views
from .views import predict

urlpatterns = [
    path('', predict, name='predict'),
]