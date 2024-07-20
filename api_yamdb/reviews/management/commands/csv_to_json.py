from django.core.management.base import BaseCommand, CommandError
from utils.csv_to_json_fixture import csv_to_json


class Command(BaseCommand):
    """
    Регистрация кастомной django-admin команды.
    Она вызывает функцию конвертации csv в json django фикстуры.

    Находясь тут:
    ~/api_yamdb/api_yamdb/

    Запускаем так:
    python3 manage.py csv_to_json \
        --csv_path='static/data/' \
        --json_path='static/fixtures/'

    , либо так:
    python3 manage.py csv_to_json
    """

    help = 'Конвертирует csv файлы в json фикстуры для Django'

    def add_arguments(self, parser):
        """
        Добавляем опциональные аргументы командной строки.
        :param parser: Собственно, сами аргументы парсера.
        """
        parser.add_argument(
            '--csv_path',
            type=str,
            default='static/data/',
            help='Относительный путь к директории CSV файлов',
        )
        parser.add_argument(
            '--json_path',
            type=str,
            default='static/fixtures/',
            help='Относительный путь к директории для '
            'генерации JSON DB фикстур',
        )

    def handle(self, *args, **options):
        """
        Хендлер django-admin, который вызывает функцию конвертации csv в json.
        :param args: Неименованные аргументы.
        :param options: Именованные аргументы.
        """
        try:
            csv_to_json(self, **options)
        except Exception as e:
            CommandError(f'Возникла какая-то ошибка: {e}')
