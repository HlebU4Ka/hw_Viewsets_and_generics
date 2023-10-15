from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseListView, CourseDetailView, CourseViewSet, LessonListCreateView, LessonDetailView, \
    LessonViewSet, CustomTokenObtainView, YourView

# Создаем роутер для автоматического создания URL-маршрутов для ViewSet'ов
router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('api/token/', CustomTokenObtainView.as_view(), name='token_obtain'),
    path('your-view/', YourView.as_view(), name='your_view'),
    path('', include(router.urls)),
]