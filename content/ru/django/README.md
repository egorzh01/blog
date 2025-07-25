# DJANGO v5

Буду идти по шагам, создавая приложение на django.

Для начала необходимо различать 2 подхода к созданию веб приложений:

1. SSR

   Сервер сам работает с данными, отдает эти данные в шаблон, рендерит(Работает с данными внутри шаблона) и отдает готовую страницу(готовый HTML) браузеру.

   В этом случае мы используем Django. Он предоставляет большой набор готовых решений для разработки SSR.

2. API

   Сервер работает только с данными. Принимает и отдает данные в разных форматах(например `JSON` или `XML`). Работать вручную, без специального UI очень не удобно. Поэтому веб приложение делиться на `frontend`(ui) и `backend`(server). Фронтенд запрашивает данные у `backend` и сам размещает на странице браузера. Либо делает запросы на изменение на тот же `backend`. В свою очередь, `backend` работает с базой данных, запускает периодические задачи, [сериализует](../footnotes/README.md#сериализация), [дисериализует](../footnotes/README.md#десериализация) и [валидирует](../footnotes/README.md#валидация), в общем работает только с сырыми данными.

   - Также как одна реализаций API есть REST API. Он предоставляет правила для создания и работы с таким API. Здесь у нас есть Django Rest Framework(DRF). Он также предоставляет готовые инстсрументы для создания REST API.

## Начало работы

### Установка:

Скачиваем в нашу виртуальную среду `django`.

```bash
pip install django
poetry add django
uv add django
```

### После установки:

Проект Django создаётся с помощью утилиты `django-admin`, которая устанавливается вместе с Django и размещается в папке `bin` виртуальной среды(например в `.venv/bin/`). Это позволяет использовать её после активации окружения.

```bash
django-admin startproject mysite
```

Эта команда создаёт новую папку mysite, внутри которой уже будет заготовка проекта:

```
mysite/                  ← создана автоматически
├── mysite/              ← конфигурационная директория проекта
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```

### Использование кастомной корневой папки

Вместо того чтобы позволить Django создать внешнюю папку, мы часто создаём её заранее сами (например, с помощью uv), а затем инициализируем Django внутри неё командой:

```bash
django-admin startproject config .
```

Здесь:

- `config` — имя директории, в которую будут помещены конфигурационные файлы проекта;

- `.` — означает, что проект будет инициализирован в текущей директории, а не во вновь созданной.

После выполнения команды структура будет следующей:

```
ourproject/              ← папка, созданная вручную
├── config/              ← конфигурация проекта
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```

---

**О папке config**

Мы указали config как имя проекта, чтобы папка с конфигурационными файлами называлась осмысленно. Хотя по умолчанию её часто называют так же, как и весь проект (например, mysite), использование названия config помогает чётко отразить её назначение — хранение настроек и конфигурации.

Вы можете выбрать любое имя, главное — не конфликтовать с именами Python-модулей и сохранять логичную структуру.

---

### Обзор структуры проекта

#### _config/_

Папка с основными конфигурациями проекта. Мы задали имя `config`, чтобы подчеркнуть её назначение — **хранение настроек и конфигурационных файлов**.

#### _config/settings.py_

Файл настроек проекта. Здесь задаются:

- базовые параметры (например, `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`);
- конфигурация баз данных;
- путь к статике и медиафайлам;
- список установленных приложений (`INSTALLED_APPS`);
- мидлвари, шаблоны и другие глобальные параметры.

Этот модуль определяет поведение проекта во всех средах (разработка, тестирование, прод).

#### _config/urls.py_

Файл маршрутизации. Здесь определяется **главный URL-конфиг**, в который можно включать маршруты из других приложений. По сути, это точка входа для системы обработки запросов.

#### _config/wsgi.py_

Файл конфигурации для **WSGI** (Web Server Gateway Interface).

Django-приложение само по себе не принимает запросы и не отправляет ответы — этим занимается внешний **веб-сервер** (например, Gunicorn или uWSGI), который взаимодействует с приложением через WSGI.

Этот интерфейс позволяет запускать Django в **синхронном режиме** на классических веб-серверах.

#### _config/asgi.py_

Файл конфигурации для **ASGI** (Asynchronous Server Gateway Interface).

Аналог WSGI, но предназначен для **асинхронных приложений** и серверов (например, Uvicorn или Daphne).  
Используется, если вы планируете задействовать WebSocket, фоновые задачи или асинхронные вьюхи.

#### _manage.py_

Командная утилита для управления проектом.

С её помощью можно:

- запускать сервер разработки (`runserver`);
- выполнять миграции (`migrate`, `makemigrations`);
- создавать приложения (`startapp`);
- работать с базой данных (`dbshell`, `inspectdb`);
- запускать тесты и собственные CLI-команды.

Этот файл — основная точка входа для работы с проектом через командную строку.

## Типизация Django

Django изначально слабо типизирован — во многих местах отсутствуют аннотации типов, что затрудняет использование статического анализа и автодополнения в IDE.

Чтобы повысить надежность кода и удобство разработки, мы устанавливаем стабы — .pyi-файлы, содержащие только типовую информацию. Они не влияют на выполнение программы, но позволяют инструментам, таким как mypy и современные редакторы кода (VS Code, PyCharm), лучше понимать структуру Django и подсказывать допустимые типы, методы и атрибуты.

Стабами можно расширить типизацию сторонних библиотек без изменения их исходного кода.

```bash
pip install django-stubs
poetry add --group dev django-stubs
uv add --dev django-stubs
```

Скачиваем также _django-stubs-ext_ как продовскую зависимость.

```bash
pip install django-stubs-ext
poetry add django-stubs-ext
uv add django-stubs-ext
```

В нашем файле _config/settings.py_ добавляем:

```python
import django_stubs_ext

django_stubs_ext.monkeypatch()
```

Это позволит в будущем делать вещи по типу `QuerySet[MyModel]`(Что такое QuerySet будет позже). Без этого действия эта аннотация вызовет ошибку.

Также можно настроить mypy с этой библиотекой, если интересно можно [почитать](https://github.com/typeddjango/django-stubs).

Пробуем запустить наше приложение с сервером, на данном этапе мы просто должны увидеть начальную страницу django для подтверждения чтомы:

```bash
python manage.py runserver
```

**ВАЖНО**: Таким образом запускается облегченный веб сервер который обслуживает наше приложение. Используется только для разработки. Продакшн среду он не потянет. Для этого используется веб-сервер _gunicorn_ или др.

```bash
pip install gunicorn
poetry add gunicorn
uv add gunicorn
```

Запуск нашего приложения теперь выглядит так:

```bash
gunicorn config.wsgi:application
```

Это запустит один процесс, выполняющий один поток, прослушивающий _127.0.0.1:8000_.

### Создание приложения

Один из ключевых принципов Django — разделение проекта на независимые компоненты, называемые **приложениями**. Каждое приложение отвечает за одну логически завершённую часть функциональности.

📌 Когда стоит создавать отдельное приложение?

Создавайте новое приложение, если:

- Это самостоятельный модуль, который может быть использован повторно (например, блог, корзина, система комментирования, личный кабинет и т.п.).

- Функциональность чётко разделяется по смыслу и может иметь собственные модели, представления и маршруты.

- Вы планируете тестировать или развивать эту часть отдельно.

🚫 Когда не стоит создавать новое приложение?

- Если функциональность слишком мелкая и не имеет смысла как отдельный модуль.

- Если это просто часть логики уже существующего приложения (например, фильтрация в каталоге товаров — это часть "catalog", а не отдельное приложение "filters").

- Если это приведёт к избыточной дробности, которая усложнит структуру проекта.

Для создания нового приложения используем команду:

```bash
python manage.py startapp myapp
```

Будет создана базовая структура:

```
myapp/
├── admin.py
├── apps.py
├── models.py
├── tests.py
├── views.py
├── migrations/
│   └── __init__.py
└── __init__.py
```

Однако в большинстве реальных проектов структура приложения со временем расширяется:

```
myapp/
├── __init__.py
├── admin.py              ← регистрация моделей в админке
├── apps.py               ← конфигурация приложения
├── models.py             ← ORM-модели
├── views.py              ← контроллеры (обработчики запросов)
├── urls.py               ← маршруты приложения
├── forms.py              ← Django-формы
├── serializers.py        ← DRF-сериализаторы (если используете Django REST Framework)
├── permissions.py        ← пользовательские разрешения
├── filters.py            ← фильтры (например, для django-filter)
├── signals.py            ← сигналы (например, post_save)
├── services.py           ← бизнес-логика, работа с внешними API
├── tasks.py              ← Celery-задачи
├── utils.py              ← вспомогательные функции
├── tests/                ← модульные и интеграционные тесты
│   └── ...
├── templates/            ← HTML-шаблоны (если используются)
│   └── myapp/
├── static/               ← статические файлы (CSS, JS, изображения)
│   └── myapp/
└── migrations/           ← миграции для моделей
    └── __init__.py
```

### Создание моделей

Django-проекты в первую очередь работают с данными: создают, хранят, изменяют и отображают их. Для этого Django предоставляет мощную **ORM** (Object-Relational Mapping) систему.

---

#### Что такое ORM?

**ORM (Object-Relational Mapping)** — это технология, позволяющая работать с базой данных через объектно-ориентированный подход.
Вместо написания SQL-запросов напрямую мы описываем **модели** в виде обычных Python-классов, а Django автоматически переводит их в SQL, создаёт таблицы, выполняет запросы и т.д.

> Пример: класс `User` в Python превращается в таблицу `user` в базе данных, а поля класса — в столбцы таблицы.

---

#### Как создать модель

Модели описываются в файле `models.py` приложения. Все модели наследуются от базового класса `django.db.models.Model`.

```python
# myapp/models.py

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```

---

#### Типичные поля модели

| Поле              | Описание                                    |
| ----------------- | ------------------------------------------- |
| `CharField`       | Строка фиксированной длины                  |
| `TextField`       | Длинный текст                               |
| `IntegerField`    | Целое число                                 |
| `DecimalField`    | Десятичное число (точнее, чем `FloatField`) |
| `DateTimeField`   | Дата и время                                |
| `BooleanField`    | Логическое значение                         |
| `ForeignKey`      | Внешний ключ (связь многие-к-одному)        |
| `ManyToManyField` | Связь многие-ко-многим                      |
| `OneToOneField`   | Один-к-одному                               |

---

#### Что делать после создания модели

1. **Создать миграции** (инструкции для базы данных на основе модели):

   ```bash
   python manage.py makemigrations
   ```

2. **Применить миграции** (создать таблицы в БД):

   ```bash
   python manage.py migrate
   ```

   > При установке, django также автоматически принес с собой другие миграции которые связаны со стандартными приложениями django такими как `auth`, `contenttypes` и `sessions`.

---

#### Работа с моделями

Создание объекта:

```python
product = Product.objects.create(name="Товар", price=199.99)
```

Получение объектов:

```python
Product.objects.all()                         # Все записи
Product.objects.get(id=1)                     # Один объект
Product.objects.filter(price__lt=1000)        # Фильтрация
Product.objects.order_by('-created_at')       # Сортировка
```

Изменение:

```python
product = Product.objects.get(id=1)
product.price = 149.99
product.save()
```

Удаление:

```python
product.delete()
```

---

> 📌 Рекомендуется каждый класс-модель делать в отдельном приложении, если он логически обособлен (например, `User`, `Product`, `Order`, `BlogPost`, и т.д.).

### Создание суперпользователя

Изначально `Django` уже подготовил набор предустановленных моделей, включающих `User`.

Мы можем создать суперпользователя командой

```bash
python manage.py createsuperuser
```

#### Кастомизация пользователя

...

### Панель администратора

...

### Создание контроллеров

Основной частью нашего приложения, являются контроллеры, которые будут обрабатывать запросы пользователя.

```python
# myapp/views.py

from django.http import HttpResponse, HttpRequest

def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello, world!")
```

### Создание маршрутов

Для того чтобы приложение могло понять какой хендлер должен обрабатывать запрос, необходимо создать маршруты.

```python
# myapp/urls.py

from django.urls import path

urlpatterns = [
    path("", index, name="index"),
]
```

Далее нам нужно подключить маршруты к нашему приложению:

```python
# myapp/apps.py

from django.apps import AppConfig

class MyappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "myapp"

    def ready(self):
        import myapp.urls
```
