from rest_framework import serializers
from .models import Lesson, Course


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Lesson.
    """

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview_image', 'video_links', 'materials']


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Course.
    """

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview_image', 'description']
