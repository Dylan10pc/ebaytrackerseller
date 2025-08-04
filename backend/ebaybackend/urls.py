from django.urls import path
from .views import test_api
from . import views

urlpatterns = [
    path('auth/init/', views.initiate_auth),
    path('auth/callback/', views.auth_callback),
]