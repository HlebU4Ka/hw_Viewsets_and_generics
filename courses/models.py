from django_filters import rest_framework as filters
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


avatar_settings = {'null': True, 'blank': True}


class Course(models.Model):
    """Модель для курса."""
    objects = None
    title = models.CharField(max_length=100)
    preview_image = models.ImageField(upload_to='course_previews/', **avatar_settings)
    description = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Возвращает строковое представление курса."""
        return self.title


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
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

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
    user = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} subscribed to {self.course}'


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
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    date_paid = models.DateTimeField(verbose_name="Дата оплаты")
    paid_item = models.ForeignKey(
        models.Q(course__isnull=False) and Course or Lesson,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный курс или урок"
    )
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
