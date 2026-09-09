# 🚀 Smart Code — Платформа для обучения программированию

Учебная платформа в стиле Codewars/LeetCode для школ и курсов программирования. Ученики решают задачи на Python, учителя создают задачи (в том числе с помощью AI), назначают их классам и отслеживают прогресс.

## Основные фичи

- 🎯 **Каталог задач** — задачи с уровнями сложности (Easy / Medium / Hard), тегами и фильтрацией
- 🤖 **AI-ментор** — подсказки, code review и генерация задач через Google Gemini
- ⚔️ **Code Battles** — PvP-дуэли 1 на 1 в реальном времени
- 🏆 **Геймификация** — XP, уровни, стрики, достижения
- 📊 **Аналитика для учителей** — матрица сдачи заданий, экспорт в CSV
- 👥 **Классы** — учитель создаёт класс, ученики присоединяются по коду

## Требования

- Python 3.11+
- Django 5.2+

## Установка и запуск

```bash
# 1. Клонировать репозиторий
git clone <url> && cd Smart_code

# 2. Создать и активировать виртуальное окружение
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Настроить переменные окружения
cp .env.example .env
# Отредактировать .env — указать DJANGO_SECRET_KEY и GEMINI_API_KEY

# 5. Применить миграции
python manage.py migrate

# 6. Создать базовые достижения
python manage.py seed_achievements

# 7. Создать суперпользователя (опционально)
python manage.py createsuperuser

# 8. Запустить сервер
python manage.py runserver
```

Приложение будет доступно по адресу: http://127.0.0.1:8000/

## Переменные окружения

| Переменная | Описание | Пример |
|---|---|---|
| `DJANGO_SECRET_KEY` | Секретный ключ Django (обязательно) | `your-random-secret-key` |
| `DJANGO_DEBUG` | Режим отладки | `True` / `False` |
| `DJANGO_ALLOWED_HOSTS` | Разрешённые хосты | `127.0.0.1,localhost` |
| `GEMINI_API_KEY` | API-ключ Google Gemini | `AIza...` |

## Структура проекта

```
Smart_code/
├── core/              # Настройки Django (settings, urls)
├── accounts/          # Аккаунты, профили, классы
├── challenges/        # Задачи, решения, Code Battle
│   ├── services/      # Бизнес-логика (runner, AI, геймификация)
│   ├── templatetags/  # Кастомные теги шаблонов
│   └── management/    # Management-команды
├── templates/         # Базовый шаблон (base.html)
├── scripts/           # Скрипты наполнения БД
├── requirements.txt   # Зависимости Python
└── .env.example       # Шаблон переменных окружения
```

## Тесты

```bash
python manage.py test
```

## Технологии

- **Backend**: Django 5.2, Python 3.11+
- **Frontend**: Bootstrap 5 (Dark Mode), Monaco Editor
- **AI**: Google Gemini API (google-genai SDK)
- **Безопасность**: AST-валидация кода, изолированный exec, CSRF-защита
