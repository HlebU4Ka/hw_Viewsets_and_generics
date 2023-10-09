from rest_framework import viewsets

from myproject.myproject.permissions import ModeratorPermission


class LessonViewSet(viewsets.ModelViewSet):
    permission_classes = [ModeratorPermission]
