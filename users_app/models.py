from django.db import models
from django.contrib.auth.models import User

avatar_settings = {'null': True, 'blank': True}


class UserProfile(models.Model):
    """
    Модель профиля пользователя.

    Fields:
        user (User): Связь с моделью пользователя Django.
        first_name (str): Имя пользователя.
        last_name (str): Фамилия пользователя.
        date_of_birth (date): Дата рождения пользователя.
        country (str): Страна пользователя.
        courses (ManyToManyField): Список курсов, на которые подписан пользователь.
        avatar (ImageField): Аватар пользователя.
        is_moderator (bool): Флаг, указывающий, является ли пользователь модератором.

    Methods:
        __str__(): Возвращает строковое представление объекта.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=50, blank=True)
    courses = models.ManyToManyField('courses.Course', blank=True)
    avatar = models.ImageField(upload_to='avatars/', **avatar_settings)
    is_moderator = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        """
        Возвращает строковое представление объекта.

        Returns:
            str: Строковое представление объекта (email и имя пользователя).
        """
        return f"{self.user.email} - {self.first_name} {self.last_name}"
