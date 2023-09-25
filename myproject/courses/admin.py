from django.contrib import admin
from .models import Course, Lesson, CustomUser

# Register your models here.
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(CustomUser)
