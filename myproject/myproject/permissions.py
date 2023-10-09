from rest_framework import permissions


class ModeratorPermission(permissions.BasePermission):
    """
    Разрешает просмотр всем пользователям (GET запросы).
    Разрешает редактирование (PUT, PATCH) только модераторам.
    """

    def has_permission(self, request, view):
        # Разрешаем просмотр всем пользователям
        if request.method == 'GET':
            return True

        # Разрешаем редактирование только модераторам
        if request.user and request.user.is_moderator:
            # Для редактирования объектов
            if request.method in ['PUT', 'PATCH']:
                return True

        # Запрещаем остальные методы (добавление, удаление)
        return False


class CourseAndLessonPermission(permissions.BasePermission):
    """
    Разрешает просмотр всем пользователям (GET, HEAD, OPTIONS).
    Разрешает редактирование объектов только владельцам курса или урока.
    Для других методов (добавление, удаление) доступ запрещен."""

    def has_permission(self, request, view):
        # Проверка, является ли пользователь модератором
        if request.user and request.user.is_moderator:
            return True

        # Для других пользователей разрешаем только безопасные методы (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        # Разрешаем, если пользователь является владельцем курса или урока
        return obj.user == request.user


class IsOwnerOrModerator(permissions.BasePermission):
    """
       Пользовательское разрешение для разрешения владельцам и модераторам редактировать объект.
       """

    def has_object_permission(self, request, view, obj):
        """
        Проверяет, имеет ли пользователь разрешение на редактирование объекта.

        Args:
            request (HttpRequest): HTTP-запрос.
            view (APIView): Просмотр, запрашивающий проверку.
            obj (object): Объект, к которому осуществляется доступ.

        Returns:
            bool: True, если пользователь может редактировать объект, в противном случае False.
        """
        # Модераторы могут редактировать любые объекты
        if request.user and request.user.is_moderator:
            return True

        # Пользователи могут редактировать только свои объекты
        return obj.user == request.user
