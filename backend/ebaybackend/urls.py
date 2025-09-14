from django.urls import path

from . import views

urlpatterns = [
    path('auth/init/', views.initiate_auth),
    path('auth/callback/', views.auth_callback),
]