from django.db import models
avatar_settings = {'null': True, 'blank': True}


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


