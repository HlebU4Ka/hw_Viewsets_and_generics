from django.db import models
from django.core.exceptions import ValidationError

from myproject.myproject.utils import is_youtube_link
from myproject.users_app.models import UserProfile

avatar_settings = {'null': True, 'blank': True}


class Course(models.Model):
    """Модель для курса."""
    objects = None
    title = models.CharField(max_length=100)
    preview_image = models.ImageField(upload_to='course_previews/', **avatar_settings)
    description = models.CharField(max_length=255)

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
            user (UserProfile): Связь с профилем пользователя.
            course (Course): Связь с курсом, на который подписан пользователь.
            subscribed_at (datetime): Время подписки пользователя.

        Methods:
            __str__(): Возвращает строковое представление объекта.

        """

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} subscribed to {self.course}'
