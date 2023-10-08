from django.urls import path
from . import views
from .serialazers import UserProfileDetail

urlpatterns = [
    path('profile/<int:pk>/', views.UserProfileDetail.as_view(), name='user-profile-detail')
]