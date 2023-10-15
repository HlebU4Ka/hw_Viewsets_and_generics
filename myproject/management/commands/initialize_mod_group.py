from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    """
    Команда Django для инициализации группы модераторов с соответствующими правами.

    Использование:
    python manage.py initialize_mod_group

    """
    help = 'Инициализировать группу модераторов с соответствующими правами'

    def handle(self, *args, **kwargs):
        """
        Обработка команды для создания группы модераторов и назначения прав.

        Аргументы:
            *args: Дополнительные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        """
        # Создаем группу модераторов
        moderator_group, created = Group.objects.get_or_create(name='Модераторы')

        # Получаем разрешения на просмотр и изменение уроков и курсов
        lesson_view_permission = Permission.objects.get(codename='view_lesson')
        lesson_change_permission = Permission.objects.get(codename='change_lesson')
        course_view_permission = Permission.objects.get(codename='view_course')
        course_change_permission = Permission.objects.get(codename='change_course')

        # Добавляем разрешения к группе модераторов
        moderator_group.permissions.add(lesson_view_permission)
        moderator_group.permissions.add(lesson_change_permission)
        moderator_group.permissions.add(course_view_permission)
        moderator_group.permissions.add(course_change_permission)

        # Сохраняем изменения
        moderator_group.save()

        self.stdout.write(self.style.SUCCESS('Группа модераторов успешно инициализирована.'))
