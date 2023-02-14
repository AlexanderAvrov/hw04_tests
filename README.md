# Тесты для проекта YaTube

Покрытие тестами проекта Yatube. 

Стек:
- Python 3.7
- django-debug-toolbar 2.2
- django 2.2.16
- pytest-django 3.8.0
- pytest-pythonpath 0.7.3
- pytest 5.3.5
- requests 2.22.0
- six 1.14.0
- sorl-thumbnail 12.6.3
- mixer 7.1.2
- pillow==9.2.0

Устанавливаем виртуальное окружение:

```bash
python -m venv venv
```

Активируем виртуальное окружение:

```bash
source venv/Scripts/activate
```

Устанавливаем зависимости:

```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

Для запуска тестов:

```bash
pytest
```

Запускаем проект:

```bash
python yatube/manage.py runserver
```

После чего проект будет доступен по адресу http://localhost:8000/
