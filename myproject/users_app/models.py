from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User

from myproject.courses.models import Course

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
    courses = models.ManyToManyField(Course, blank=True)
    avatar = models.ImageField(upload_to='avatars/', **avatar_settings)
    is_moderator = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return f"{self.user.email} - {self.first_name} {self.last_name}"


class CustomUserManager(BaseUserManager):
    """
        Кастомный менеджер пользователя.

        Methods:
            create_user(): Создает пользователя.
            create_superuser(): Создает суперпользователя.

        """
    def create_user(self, email, password=None, **extra_fields):
        """
               Создает пользователя.

               Args:
                   email (str): Email пользователя.
                   password (str): Пароль пользователя.
                   **extra_fields: Дополнительные поля пользователя.

               Raises:
                   ValueError: Если email не указан.

               """
        if not email:
            raise ValueError('Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  # Fixed the typo here

    def create_superuser(self, email, password=None, **extra_fields):
        """
               Создает суперпользователя.

               Args:
                   email (str): Email суперпользователя.
                   password (str): Пароль суперпользователя.
                   **extra_fields: Дополнительные поля суперпользователя.

               """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    """
       Кастомная модель пользователя.

       Fields:
           email (str): Email пользователя.
           phone (str): Телефон пользователя.
           city (str): Город пользователя.

       """
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=13)
    city = models.CharField(max_length=100)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'city']
