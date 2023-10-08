from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Lesson, Course, Subscription
from django.contrib.auth.models import User


class LessonAPITestCase(APITestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(username='testuser', password='password')
        # Создаем курс
        self.course = Course.objects.create(title='Test Course', description='Test Description')
        # Создаем урок
        self.lesson = Lesson.objects.create(title='Test Lesson', description='Test Lesson Description',
                                            course=self.course)

    def test_get_lesson_list(self):
        url = reverse('lesson-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_lesson_detail(self):
        url = reverse('lesson-detail', kwargs={'pk': self.lesson.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Добавьте тесты для создания, обновления и удаления уроков


class CourseAPITestCase(APITestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(username='testuser', password='password')
        # Создаем курс
        self.course = Course.objects.create(title='Test Course', description='Test Description')

    def test_get_course_list(self):
        url = reverse('course-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_course_detail(self):
        url = reverse('course-detail', kwargs={'pk': self.course.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Добавьте тесты для создания, обновления и удаления курсов


class SubscriptionAPITestCase(APITestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(username='testuser', password='password')
        # Создаем курс
        self.course = Course.objects.create(title='Test Course', description='Test Description')

    def test_subscribe_course(self):
        url = reverse('subscribe-course', kwargs={'pk': self.course.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unsubscribe_course(self):
        subscription = Subscription.objects.create(user=self.user, course=self.course)
        url = reverse('unsubscribe-course', kwargs={'pk': self.course.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
