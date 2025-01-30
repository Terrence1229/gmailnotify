# example/urls.py
from django.urls import path

from . import views
from .gmail import MAPIView

urlpatterns = [
    path('', views.index),
    path('test', views.test),
    path('authcallback', MAPIView.authcallback)
]