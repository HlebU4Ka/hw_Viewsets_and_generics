from rest_framework import serializers
from .models import Course, Lesson, Payment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class LessonSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    # Добавляем поле для количества уроков
    num_lessons = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Course
        fields = '__all__'

    def get_num_lessons(self, obj):
        # Получаем количество уроков для данного курса
        return obj.lesson_set.count()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Персонализированный сериализатор для включения
    дополнительной информации о пользователе
    в ответе токена.
    """

    def validate(self, attrs):
        """
        Переопределенный метод проверки данных.

        Args:
            attrs (dict): Атрибуты запроса.

        Returns:
            dict: Данные для ответа.

        """
        data = super().validate(attrs)
        data['username'] = self.user.usernam
        data['password'] = self.user.password

        return data
