from django_filters import rest_framework as filters
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from users_app.models import UserProfile

avatar_settings = {'null': True, 'blank': True}


class Course(models.Model):
    """Модель для курса."""
    objects = None
    title = models.CharField(max_length=100)
    preview_image = models.ImageField(upload_to='course_previews/', **avatar_settings)
    description = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              default=1)

    def __str__(self):
        """Возвращает строковое представление курса."""
        return self.title


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)

    def __str__(self):
        return self.username


class LessonManager(models.Manager):
    """Менеджер для управления уроками."""

    def active_lessons(self):
        """Возвращает активные уроки."""
        return self.filter(active=True)


class Lesson(models.Model):
    """Модель для урока."""
    title = models.CharField(max_length=100)
    description = models.TextField()
    preview_image = models.ImageField(upload_to='lesson_previews/', **avatar_settings)
    video_links = models.URLField()
    materials = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    def save(self, *args, **kwargs):
        """
        Переопределенный метод сохранения урока.

        Проверяет каждую ссылку в материалах и разрешает только ссылки на YouTube.

        Args:
            *args: Аргументы.
            **kwargs: Ключевые аргументы.

        Raises:
            ValidationError: Если найдены ссылки на сторонние ресурсы, отличные от YouTube.

        """
        # Проверка каждой ссылки в материалах
        from myproject.utils import is_youtube_link
        for link in self.materials.split('\n'):
            if not is_youtube_link(link):
                raise ValidationError('В материалах разрешены только ссылки на YouTube.')
        super().save(*args, **kwargs)

    objects = LessonManager()

    def __str__(self):
        """Возвращает строковое представление урока."""
        return self.title


class Subscription(models.Model):
    """
    Модель подписки пользователя на курс.

    Fields:
        user (str): Строковое имя пользователя.
        course (Course): Связь с курсом, на который подписан пользователь.
        subscribed_at (datetime): Время подписки пользователя.

    Methods:
        __str__(): Возвращает строковое представление объекта.

    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} подписан на {self.course.title}"


class CourseManager(models.Manager):
    """
    Менеджер для управления курсами.

    Методы:
        active_courses(): Получает активные курсы.

    """

    def active_courses(self):
        """
        Получает активные курсы.

        Returns:
            QuerySet: Активные курсы.

        """
        return self.filter(active=True)


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь", default=1)
    date_paid = models.DateTimeField(verbose_name="Дата оплаты")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    paid_item = GenericForeignKey('content_type', 'object_id')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма оплаты")
    payment_method = models.CharField(
        max_length=20,
        choices=[
            ('cash', 'Наличные'),
            ('bank_transfer', 'Банковский перевод'),
        ],
        verbose_name="Способ оплаты"
    )

    # Новые поля из приложения courses
    some_course_field = models.CharField(max_length=100, verbose_name="Дополнительное поле из курса", blank=True)
    some_lesson_field = models.CharField(max_length=100, verbose_name="Дополнительное поле из урока", blank=True)

    def __str__(self):
        return f'Платеж за {self.paid_item} от {self.user}'

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"


class PaymentFilter(filters.FilterSet):
    course = filters.CharFilter(field_name='paid_item', method='filter_course')
    lesson = filters.CharFilter(field_name='paid_item', method='filter_lesson')
    payment_method = filters.CharFilter(field_name='payment_method')

    class Meta:
        model = Payment
        fields = []

    def filter_course(self, queryset, name, value):
        return queryset.filter(paid_item__course__title=value)

    def filter_lesson(self, queryset, name, value):
        return queryset.filter(paid_item__lesson__title=value)
