# User Authentication API

## Описание

Простой API для регистрации, аутентификации и управления пользователями с использованием FastAPI, PostgreSQL и асинхронного SQLAlchemy.

---

## Особенности

- Регистрация пользователей с безопасным хэшированием пароля (bcrypt)
- Вход с выдачей JWT access-токена с коротким сроком действия (5 минут)
- Обновление пользовательских данных
- Логическое удаление (деактивация) пользователя
- Поддержка ролей пользователя (user, admin) через Enum
- Асинхронное взаимодействие с базой данных SQLAlchemy
- Валидация и сериализация с помощью Pydantic

---

## Запуск проекта

1. Клонировать репозиторий
2. Создать и активировать виртуальное окружение
3. Установить зависимости:
```bash
pip install -r requirements.txt
```

4. Создать файл `.env` с параметрами подключения и секретным ключом:

```bash
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
SECRET_KEY=your_secret_key_here
```

5. Запустить сервер:

```bash
uvicorn main:app --host 127.0.0.1 --port 8080 --reload
```

---

## Эндпоинты API

- POST `/register` — регистрация нового пользователя
- POST `/login` — вход с получением JWT токена
- PUT `/user/{user_id}` — обновление данных пользователя
- DELETE `/user/{user_id}` — деактивация пользователя (удаление)
- POST `/logout` — выход (ключевой функционал зависит от реализации)

---

## Технологии

- Python 3.13
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- PassLib (bcrypt)
- python-jose (JWT)
- Pydantic
