from django.shortcuts import render
from django.views import View
from rest_framework import generics, viewsets
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Пользователь может редактировать только свой профиль.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Разрешено только администраторам.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class UserProfileDetailView(View):
    """Представление для отображения деталей профиля пользователя."""
    permission_classes = [IsOwnerOrReadOnly, IsStaffOrReadOnly]
    def get(self, request, pk):
        """Обрабатывает GET-запрос для отображения конкретного профиля пользователя."""
        user_profile = UserProfile.objects.get(pk=pk)
        return render(request, 'users_app/user_profile_detail.html', {'user_profile': user_profile})


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet для выполнения операций CRUD над профилями пользователей."""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrReadOnly, IsStaffOrReadOnly]


class UserProfileListCreateView(generics.ListCreateAPIView):
    """Представление для отображения списка профилей пользователей и создания новых профилей."""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrReadOnly, IsStaffOrReadOnly]

class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Представление для получения, обновления и удаления профиля пользователя."""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileListView(generics.ListAPIView):
    """Представление для отображения списка профилей пользователей."""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrReadOnly, IsStaffOrReadOnly]

