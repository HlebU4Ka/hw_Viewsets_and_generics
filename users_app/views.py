from django.shortcuts import render
from django.views import View
from rest_framework import generics, viewsets
from .models import UserProfile
from .serializers import UserProfileSerializer


class UserProfileDetailView(View):
    """Представление для отображения деталей профиля пользователя."""

    def get(self, request, pk):
        """Обрабатывает GET-запрос для отображения конкретного профиля пользователя."""
        user_profile = UserProfile.objects.get(pk=pk)
        return render(request, 'users_app/user_profile_detail.html', {'user_profile': user_profile})


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet для выполнения операций CRUD над профилями пользователей."""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileListCreateView(generics.ListCreateAPIView):
    """Представление для отображения списка профилей пользователей и создания новых профилей."""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Представление для получения, обновления и удаления профиля пользователя."""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileListView(generics.ListAPIView):
    """Представление для отображения списка профилей пользователей."""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
