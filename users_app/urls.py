from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, UserProfileListCreateView, UserProfileDetailView, UserProfileListView

router = DefaultRouter()
router.register(r'userprofiles', UserProfileViewSet)

urlpatterns = [
    path('userprofiles/', UserProfileListCreateView.as_view(), name='userprofile-list-create'),
    path('userprofiles/<int:pk>/', UserProfileDetailView.as_view(), name='userprofile-detail'),
    path('userprofiles-list/', UserProfileListView.as_view(), name='userprofile-list'),
    path('', include(router.urls)),
]
