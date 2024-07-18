import csv
import json
from os import listdir
from os.path import isfile, join

MODEL_MAPPING = {
    'users.csv': 'auth.user',
    'genre.csv': 'reviews.genre',
    'titles.csv': 'reviews.title',
    'comments.csv': 'reviews.comment',
    'review.csv': 'reviews.review',
    'genre_title.csv': 'reviews.title.genre',
    'category.csv': 'reviews.category',
}


def make_json(csv_path: str, json_path: str, model_name: str) -> None:
    """
    Конвертирует csv файл в json фикстуру.
    :param csv_path: путь к csv файлу
    :param json_path: путь к json фикстуре
    :param model_name: имя модели Django
    """
    data = []
    pk_counter = 1  # счетчик для установки первичного ключа
    json_entire_path = join(
        json_path, csv_path.split('/')[-1].split('.')[0] + '.json'
    )
    print(f'Фикстура {json_entire_path} модели {model_name} создается...')

    with open(csv_path, encoding='utf-8') as csvf:
        csv_rows = csv.DictReader(csvf)
        for row in csv_rows:
            fixture_entry = {
                "model": model_name,
                "pk": pk_counter,
                "fields": row,
            }
            data.append(fixture_entry)
            pk_counter += 1

    with open(json_entire_path, 'w', encoding='utf-8') as jsonf:
        json.dump(data, jsonf, ensure_ascii=False, indent=4)
        print(f'Фикстура {json_entire_path} модели {model_name} создана')


def csv_to_json(
    csv_path: str = 'static/data/', json_path: str = 'static/fixtures/'
) -> None:
    """
    Конвертирует csv файлы в json фикстуры.
    :param csv_path: путь к csv файлам
    :param json_path: путь к json db фикстурам
    """
    csv_files = [f for f in listdir(csv_path) if isfile(join(csv_path, f))]
    print(f'Следующие CSV файлы будут конвертированы в JSON: {csv_files}')

    for csv_file in csv_files:
        model_name = MODEL_MAPPING.get(csv_file)
        if model_name:
            make_json(join(csv_path, csv_file), json_path, model_name)
        else:
            print(f'Не удалось определить модель для {csv_file}')
    print('Все CSV файлы конвертированы в JSON')


if __name__ == '__main__':
    csv_to_json()
