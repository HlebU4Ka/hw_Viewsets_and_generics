from celery import shared_task
from django.core.mail import send_mail
from courses.models import Subscription
from django.utils import timezone
from users_app.models import UserProfile


@shared_task
def send_update_notification_emails(course_title):
    """
    Отправляет уведомление об обновлении курса всем подписанным пользователям.

    Args:
        course_title (str): Название обновленного курса.

    Returns:
        None
    """
    # Получаем все активные подписки
    subscriptions = Subscription.objects.filter(active=True)

    # Отправляем уведомление каждому подписчику
    for subscription in subscriptions:
        user_email = subscription.user.email
        message = f"Привет!\n\nКурс {course_title} был обновлен."
        send_mail('Уведомление о обновлении курса', message, 'pass', [user_email])


@shared_task
def check_and_lock_inactive_users():
    # Определяем "неактивность" как отсутствие входа более месяца
    one_month_ago = timezone.now() - timezone.timedelta(days=30)

    # Находим пользователей, неактивных более месяца
    inactive_users = UserProfile.objects.filter(last_login__lte=one_month_ago, is_active=True)

    # Блокируем неактивных пользователей
    for user in inactive_users:
        user.is_active = False
        user.save()
