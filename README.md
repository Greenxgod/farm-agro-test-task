# Reproductive Farms Management System

Fullstack-приложение для управления репродуктивными показателями ферм.

## 📋 Описание

Приложение позволяет:
- Управлять списком ферм (CRUD)
- Управлять репродуктивными показателями (CRUD)
- Фильтровать и сортировать данные по ферме и датам
- Просматривать агрегированную статистику
- Работать через удобный веб-интерфейс

## 🛠 Технологический стек

### Backend
- **Python 3.11** - язык программирования
- **Flask 2.3** - веб-фреймворк
- **Flask-SQLAlchemy** - ORM
- **Flask-Migrate (Alembic)** - миграции БД
- **PostgreSQL 15** - база данных
- **Flask-CORS** - CORS поддержка
- **Flasgger** - Swagger/OpenAPI документация
- **Marshmallow** - валидация данных
- **Pytest** - тестирование

### Frontend
- **React 18** - UI библиотека
- **TypeScript** - типизация
- **Vite** - сборщик
- **TanStack Query** - управление серверным состоянием
- **React Hook Form + Zod** - формы и валидация
- **Axios** - HTTP клиент
- **CSS Modules** - стилизация

### Инфраструктура
- **Docker & Docker Compose** - контейнеризация
- **PostgreSQL** - база данных

## 📁 Структура проекта
reproductive-farms/
├── backend/ # Бекенд на Flask
│ ├── app/
│ │ ├── errors/ # Обработчики ошибок
│ │ ├── models/ # SQLAlchemy модели
│ │ ├── repositories/ # Слой доступа к данным
│ │ ├── routes/ # API эндпоинты (Blueprint)
│ │ ├── schemas/ # Marshmallow схемы
│ │ ├── services/ # Бизнес-логика
│ │ ├── init.py # Application Factory
│ │ ├── config.py # Конфигурация
│ │ ├── extensions.py # Flask расширения
│ │ └── seed.py # Заполнение тестовыми данными
│ ├── migrations/ # Alembic миграции
│ ├── tests/ # Pytest тесты
│ ├── .env.example # Пример переменных окружения
│ ├── Dockerfile # Docker образ бекенда
│ ├── requirements.txt # Python зависимости
│ └── run.py # Точка входа
│
├── frontend/ # Фронтенд на React
│ ├── src/
│ │ ├── api/ # API клиент
│ │ │ ├── dto/ # Data Transfer Objects
│ │ │ └── endpoints/ # API эндпоинты
│ │ ├── components/ # React компоненты
│ │ ├── config/ # Конфигурация
│ │ ├── hooks/ # Кастомные хуки
│ │ ├── layout/ # Layout компоненты
│ │ ├── lib/ # Утилиты (axios и т.д.)
│ │ ├── pages/ # Страницы
│ │ ├── styles/ # Глобальные стили
│ │ ├── types/ # TypeScript типы
│ │ ├── App.tsx
│ │ └── main.tsx
│ ├── .env.example # Пример переменных окружения
│ ├── Dockerfile # Docker образ фронтенда
│ ├── package.json # NPM зависимости
│ ├── vite.config.ts # Vite конфигурация
│ └── tsconfig.json # TypeScript конфигурация
│
├── docker-compose.yml # Docker Compose конфигурация
└── README.md

text

## 🔧 Переменные окружения

### Backend (.env)
```env
SECRET_KEY=dev-secret-key-12345
DATABASE_URL=postgresql://postgres:postgres@db:5432/reproductive_farms
FLASK_ENV=development
Frontend (.env)
env
VITE_API_URL=/api

🚀 Запуск через Docker Compose (Рекомендуемый способ)
bash
# Клонировать репозиторий
git clone <https://github.com/Greenxgod/farm-agro-test-task>
cd reproductive-farms

# Запустить все сервисы
docker-compose up --build

# Или в фоновом режиме
docker-compose up --build -d
После запуска:

Frontend: http://localhost:3000

Backend: http://localhost:5000

Swagger: http://localhost:5000/docs

bash
# Остановить все сервисы
docker-compose down

# Остановить и удалить данные БД
docker-compose down -v


Запуск локально (без Docker):

Backend:
bash
cd backend

# Создать и активировать виртуальное окружение
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

# Создать .env файл
cp .env.example .env

# Применить миграции
flask db upgrade

# Заполнить тестовыми данными
python -c "from app.seed import seed_database; seed_database()"

# Запустить сервер
python run.py


Frontend:
bash
cd frontend

# Установить зависимости
npm install

# Создать .env файл
cp .env.example .env

# Запустить dev сервер
npm run dev



🌱Миграции БД:
bash

cd backend

# Создать новую миграцию
flask db migrate -m "описание изменений"

# Применить миграции
flask db upgrade

# Откатить последнюю миграцию
flask db downgrade
🌱 Заполнение тестовыми данными
bash
cd backend

# Запустить seed скрипт
python -c "from app.seed import seed_database; seed_database()"

# Или через Docker
docker-compose exec backend python -c "from app.seed import seed_database; seed_database()"
Скрипт создает:

5 ферм

150 репродуктивных записей (по 30 на каждую ферму)

Данные за разные даты с разными значениями

📚 API Документация
Эндпоинты
Фермы
Метод	Эндпоинт	Описание
GET	/api/farms	Получить список ферм
GET	/api/farms/{id}	Получить ферму по ID
POST	/api/farms	Создать ферму
PUT	/api/farms/{id}	Обновить ферму
DELETE	/api/farms/{id}	Удалить ферму
Репродуктивные записи
Метод	Эндпоинт	Описание
GET	/api/reproduction-records	Получить список записей
GET	/api/reproduction-records/{id}	Получить запись по ID
POST	/api/reproduction-records	Создать запись
PUT	/api/reproduction-records/{id}	Обновить запись
DELETE	/api/reproduction-records/{id}	Удалить запись
GET	/api/reproduction-records/statistics	Получить статистику
Фильтрация, сортировка и пагинация
text
GET /api/reproduction-records?farm_id=1&date_from=2026-01-01&date_to=2026-06-01&page=1&limit=20&sort=date&order=desc
Параметры:

farm_id - фильтр по ферме

date_from - фильтр по дате (с)

date_to - фильтр по дате (по)

page - номер страницы (по умолчанию 1)

limit - записей на странице (по умолчанию 20)

sort - поле сортировки (date, farm_name)

order - порядок сортировки (asc, desc)

Ответ:

json
{
  "items": [],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
Статистика
text
GET /api/reproduction-records/statistics?farm_id=1&date_from=2026-01-01&date_to=2026-06-01
Ответ:

json
{
  "total_records": 150,
  "total_abort": 45,
  "total_dead_bulls": 12,
  "total_dead_heifers": 8,
  "avg_preg_rate_cows": 65.5,
  "avg_preg_rate_heifers": 58.2,
  "total_bulls_from_cows": 120,
  "total_bulls_from_heifers": 80,
  "total_cows_from_cows": 200,
  "total_cows_from_heifers": 150
}
Swagger документация
Интерактивная документация доступна по адресу: http://localhost:5000/docs

🧪 Тестирование
Backend тесты
bash
cd backend

# Запустить все тесты
pytest tests/ -v

# С отчетом о покрытии
pytest tests/ --cov=app --cov-report=html

# Или через Docker
docker-compose exec backend pytest tests/ -v


🐳 Docker команды
bash
# Собрать и запустить все сервисы
docker-compose up --build

# Запустить в фоне
docker-compose up --build -d

# Остановить все
docker-compose down

# Просмотр логов
docker-compose logs -f

# Зайти в контейнер бекенда
docker-compose exec backend sh

# Зайти в контейнер фронтенда
docker-compose exec frontend sh

# Подключиться к БД
docker-compose exec db psql -U postgres -d reproductive_farms


⚠️ Известные ограничения:
Отсутствует авторизация пользователей

Нет экспорта данных в CSV

Нет e2e тестов

Нет CI/CD пайплайна

Swagger требует ручной настройки для некоторых эндпоинтов

📝 Примечания:
Выбор типов данных в БД
id - Integer (автоинкремент)

name - String(100) (ограничение длины)

date - Date (только дата, без времени)

Числовые показатели - Integer (целые числа)

preg_rate_* - Float (проценты с десятичной частью)

created_at/updated_at - DateTime (автоматическое заполнение)

Валидация:

Все числовые поля ≥ 0

preg_rate_cows и preg_rate_heifers от 0 до 100

Уникальность пары (farm_id, date)

Название фермы уникально

farm_id и date обязательны для записи


Автор:
Green (Gleb Spirin)