## Описание проекта "YamDB"

Проект "YamDB" представляет собой сервис для оценки произведений. Пользователи могут оставлять отзывы и комментарии к произведениям, присваивать им оценки. Администраторы могут управлять категориями, жанрами и произведениями.

## Стек технологий

- Python
- Django
- Django REST Framework
- Simple JWT
- Git
- Redoc

### Эндпоинты

#### Авторизация и пользователи

- `POST /api/v1/auth/signup/` - регистрация нового пользователя
- `POST /api/v1/auth/token/` - получение JWT токена

#### Пользователи

- `GET /api/v1/users/` - получение списка пользователей
- `POST /api/v1/users/` - создание нового пользователя
- `GET /api/v1/users/{username}/` - получение информации о пользователе
- `PATCH /api/v1/users/{username}/` - частичное обновление информации о пользователе
- `DELETE /api/v1/users/{username}/` - удаление пользователя
- `GET /api/v1/users/me/` - получение информации о себе
- `PATCH /api/v1/users/me/` - частичное обновление информации о себе

#### Категории

- `GET /api/v1/categories/` - получение списка категорий
- `POST /api/v1/categories/` - создание новой категории
- `PATCH /api/v1/categories/{cat_slug}/` - частичное обновление информации о категории
- `DELETE /api/v1/categories/{cat_slug}/` - удаление категории

#### Жанры

- `GET /api/v1/genres/` - получение списка жанров
- `POST /api/v1/genres/` - создание нового жанра
- `PATCH /api/v1/genres/{gen_slug}/` - частичное обновление информации о жанре
- `DELETE /api/v1/genres/{gen_slug}/` - удаление жанра

#### Произведения

- `GET /api/v1/titles/` - получение списка произведений
- `POST /api/v1/titles/` - создание нового произведения
- `GET /api/v1/titles/{title_id}/` - получение информации о произведении
- `PATCH /api/v1/titles/{title_id}/` - частичное обновление информации о произведении
- `DELETE /api/v1/titles/{title_id}/` - удаление произведения

#### Отзывы

- `GET /api/v1/titles/{title_id}/reviews/` - получение списка отзывов к произведению
- `POST /api/v1/titles/{title_id}/reviews/` - создание нового отзыва к произведению
- `GET /api/v1/titles/{title_id}/reviews/{review_id}/` - получение информации о отзыве
- `PATCH /api/v1/titles/{title_id}/reviews/{review_id}/` - частичное обновление информации о отзыве
- `DELETE /api/v1/titles/{title_id}/reviews/{review_id}/` - удаление отзыва

#### Комментарии

- `GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/` - получение списка комментариев к отзыву
- `POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/` - создание нового комментария к отзыву
- `GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/` - получение информации о комментарии
- `PATCH /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/` - частичное обновление информации о комментарии
- `DELETE /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/` - удаление комментария

### Функциональность

- Регистрация и аутентификация пользователей
- Управление пользователями, категориями, жанрами и произведениями
- Оставление отзывов и комментариев к произведениям
- Подсчет средней оценки произведения при создании и обновлении отзывов
- Создана кастомная команда Django для конвертации CSV файлов в JSON фикстуры. Аргументы опциональны. Логи и разного рода нотификации удобно и красиво выводятся в консоль. Пример использования:
```bash
python3 manage.py csv_to_json --csv_path='static/data/' --json_path='static/fixtures/'
```

### Сериализация и валидация

Для сериализации данных используются специализированные сериализаторы, обеспечивающие корректное представление данных в API и их валидацию.

### Пагинация и фильтрация

Реализована пагинация для списка произведений. Доступна фильтрация по категориям, жанрам, названию произведения и году выпуска. Кастомные фильтры, права, роли и утилиты

### Применимость

Проект "YamDB" подходит для создания каталога произведений с возможностью пользовательских оценок и отзывов. Может быть использован для организации коллекций книг, фильмов, музыки и других произведений искусства.

### Запуск проекта локально

Все константные значения вынесены в отдельные переменные, включая HTTP методы, роли, HTTP статусы и другие.
Для запуска проекта локально выполните следующие шаги:

1. Клонируйте репозиторий с проектом:
```bash
git clone <url репозитория>
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Примените миграции:
```bash
python manage.py makemigrations
python manage.py migrate
```
4. Запустите сервер разработки:
```bash
python manage.py runserver
```

После выполнения этих шагов проект будет доступен по адресу `http://localhost:8000/`.

#### Контакты разработчиков

telegram: 
- [Ярослав Богданов](https://t.me/tr3fan)
- [Александр Петрушишин](https://t.me/_olexasha_)
- [Антон Савченко](https://t.me/waman204)