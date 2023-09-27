from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

avatar_settings = {'null': True, 'blank': True}


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._bd)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=13)
    city = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', **avatar_settings)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'city', 'avatar']


class Course(models.Model):
    objects = None
    title = models.CharField(max_length=100)
    preview_image = models.ImageField(upload_to='course_previews/', **avatar_settings)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class LessonManager(models.Manager):
    def active_lessons(self):
        return self.filter(active=True)


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    preview_image = models.ImageField(upload_to='lesson_previews/', **avatar_settings)
    video_links = models.URLField()

    objects = LessonManager()

    def __str__(self):
        return self.title
