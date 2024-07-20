import csv
import json
from os import listdir
from os.path import isfile, join

from django.core.management.base import BaseCommand

MODEL_MAPPING = {
    'users.csv': 'reviews.user',
    'genre.csv': 'reviews.genre',
    'titles.csv': 'reviews.title',
    'comments.csv': 'reviews.comment',
    'review.csv': 'reviews.review',
    'genre_title.csv': 'reviews.title.genre',
    'category.csv': 'reviews.category',
}

DJANGO_CMD_OBJ: BaseCommand = BaseCommand()


def wrap_print_to_stdout(
    str_print: str = "OK",
    success: bool = False,
    failure: bool = False,
    ending: str = '\n',
) -> None:
    """
    Обертывает функцию print в функцию django_obj.handle
    :param str_print: строка для печати
    :param success: флаг успешности выполнения
    :param failure: флаг неудачи выполнения
    :param ending: конец строки
    """
    if success:
        DJANGO_CMD_OBJ.stdout.write(DJANGO_CMD_OBJ.style.SUCCESS(str_print))
    elif failure:
        DJANGO_CMD_OBJ.stderr.write(DJANGO_CMD_OBJ.style.ERROR(str_print))
    else:
        DJANGO_CMD_OBJ.stdout.write(
            DJANGO_CMD_OBJ.style.WARNING(str_print), ending=ending
        )


def make_json(csv_path: str, json_path: str, model_name: str) -> None:
    """
    Конвертирует csv файл в json фикстуру.
    :param csv_path: путь к csv файлу
    :param json_path: путь к json фикстуре
    :param model_name: имя модели Django
    """
    data = []
    pk_counter = 1  # счетчик
    json_entire_path = join(
        json_path, csv_path.split('/')[-1].split('.')[0] + '.json'
    )  # парсим полный путь до json фикстур
    wrap_print_to_stdout(
        f'Фикстура {json_entire_path} модели {model_name} создается...',
        ending='',
    )

    with open(csv_path, encoding='utf-8') as csvf:
        csv_rows = csv.DictReader(csvf)
        for row in csv_rows:
            # в удобной для нас форме, учитывая кастомные
            # модели, аккуратно переводим
            fixture_entry = {
                "model": model_name,
                "pk": pk_counter,
                "fields": row,
            }
            data.append(fixture_entry)
            pk_counter += 1

    with open(json_entire_path, 'w', encoding='utf-8') as jsonf:
        json.dump(data, jsonf, ensure_ascii=False, indent=4)
        wrap_print_to_stdout(success=True)


def csv_to_json(
    django_obj: BaseCommand,
    **options,
) -> None:
    """
    Конвертирует csv файлы в json фикстуры.
    :param django_obj: объект Django Command
    :param options: дополнительные параметры
    """
    # используем глоб переменную, чтобы доставать объект Django Command
    # во всём модуле, не передавая её напрямую
    global DJANGO_CMD_OBJ
    DJANGO_CMD_OBJ = django_obj

    # принимаем именованные аргумент из командной строки и делаем их
    # удобными для нас
    csv_path = options.get('csv_path', 'static/data/')
    json_path = options.get('json_path', 'static/fixtures/')

    csv_files = [f for f in listdir(csv_path) if isfile(join(csv_path, f))]
    wrap_print_to_stdout(f'Всего CSV файлов: {len(csv_files)}', success=True)
    wrap_print_to_stdout(
        f'Следующие CSV файлы будут конвертированы в JSON: {csv_files}',
        success=True,
    )

    for csv_file in csv_files:
        model_name = MODEL_MAPPING.get(csv_file)
        if model_name:
            # пробегаемся по всем csv файлам и поочерёдно
            # конвертируем их в json
            make_json(join(csv_path, csv_file), json_path, model_name)
        else:
            wrap_print_to_stdout(
                f'Не удалось определить модель для {csv_file}', failure=True
            )
    wrap_print_to_stdout('Все CSV файлы конвертированы в JSON', success=True)
