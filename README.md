# Flask Microservices API

Учебный backend-проект, оформленный как полноценный портфолио-репозиторий: два микросервиса на Flask для работы с пользователями и заказами.

Проект демонстрирует базовые принципы микросервисной архитектуры, REST API, межсервисного HTTP-взаимодействия, валидации входных данных, обработки ошибок, тестирования и контейнеризации.

## О проекте

В системе реализованы два независимых сервиса:

- **user-service** — сервис пользователей;
- **order-service** — сервис заказов.

`order-service` обращается к `user-service`, чтобы проверить существование пользователя перед созданием заказа.

Такой подход имитирует реальное взаимодействие backend-сервисов в распределённой системе.

## Возможности

- создание пользователей;
- получение списка пользователей;
- получение пользователя по идентификатору;
- создание заказов;
- получение списка заказов;
- проверка существования пользователя перед созданием заказа;
- обработка ситуации, когда `user-service` недоступен;
- единый JSON-формат ошибок;
- валидация входных данных;
- OpenAPI-спецификация;
- Postman-коллекция;
- Docker Compose для запуска двух сервисов;
- pytest-тесты;
- GitHub Actions CI.

## Стек технологий

- Python
- Flask
- Requests
- Pytest
- Docker
- Docker Compose
- OpenAPI
- Postman
- GitHub Actions

## Структура проекта

```text
flask-microservices-api/
├── services/
│   ├── user_service/
│   │   ├── app.py
│   │   └── run.py
│   └── order_service/
│       ├── app.py
│       └── run.py
├── tests/
│   ├── test_user_service.py
│   └── test_order_service.py
├── docs/
│   ├── architecture.md
│   └── openapi.yaml
├── postman/
│   └── Flask Microservices API.postman_collection.json
├── .github/
│   └── workflows/
│       └── ci.yml
├── .env.example
├── .gitignore
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
├── LICENSE
└── README.md
```

## Архитектура

Общая схема взаимодействия:

```text
Client
  |
  | HTTP
  v
order-service
  |
  | HTTP request
  v
user-service
```

При создании заказа `order-service` получает `user_id` из запроса и отправляет запрос в `user-service`.

Если пользователь существует, заказ создаётся.  
Если пользователь не найден или сервис пользователей недоступен, клиент получает понятную JSON-ошибку.

## Установка и запуск без Docker

### 1. Клонировать репозиторий

```bash
git clone https://github.com/kindarufy/flask-microservices-api.git
cd flask-microservices-api
```

### 2. Создать виртуальное окружение

```bash
python -m venv .venv
```

### 3. Активировать виртуальное окружение

Для Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Для macOS/Linux:

```bash
source .venv/bin/activate
```

### 4. Установить зависимости

```bash
pip install -r requirements-dev.txt
```

### 5. Запустить user-service

В первом терминале:

```bash
python -m services.user_service.run
```

По умолчанию сервис будет доступен по адресу:

```text
http://127.0.0.1:5001
```

### 6. Запустить order-service

Во втором терминале для Windows PowerShell:

```powershell
$env:USER_SERVICE_URL="http://127.0.0.1:5001"
python -m services.order_service.run
```

Для macOS/Linux:

```bash
export USER_SERVICE_URL="http://127.0.0.1:5001"
python -m services.order_service.run
```

По умолчанию сервис будет доступен по адресу:

```text
http://127.0.0.1:5002
```

## Запуск через Docker Compose

```bash
docker compose up --build
```

После запуска сервисы будут доступны по адресам:

```text
user-service:  http://127.0.0.1:5001
order-service: http://127.0.0.1:5002
```

Остановить контейнеры:

```bash
docker compose down
```

## Переменные окружения

Пример переменных находится в файле `.env.example`.

Основная переменная:

```text
USER_SERVICE_URL=http://user-service:5001
```

Она используется `order-service`, чтобы обращаться к `user-service`.

## API

### User Service

#### Проверка состояния сервиса

```http
GET /health
```

Пример ответа:

```json
{
  "status": "ok",
  "service": "user-service"
}
```

#### Получить список пользователей

```http
GET /users
```

#### Получить пользователя по ID

```http
GET /users/{user_id}
```

#### Создать пользователя

```http
POST /users
Content-Type: application/json
```

Пример тела запроса:

```json
{
  "name": "Nicole",
  "email": "nicole@example.com"
}
```

Пример ответа:

```json
{
  "id": 1,
  "name": "Nicole",
  "email": "nicole@example.com"
}
```

### Order Service

#### Проверка состояния сервиса

```http
GET /health
```

Пример ответа:

```json
{
  "status": "ok",
  "service": "order-service"
}
```

#### Получить список заказов

```http
GET /orders
```

#### Создать заказ

```http
POST /orders
Content-Type: application/json
```

Пример тела запроса:

```json
{
  "user_id": 1,
  "product": "Book",
  "quantity": 2
}
```

Пример ответа:

```json
{
  "id": 1,
  "user_id": 1,
  "product": "Book",
  "quantity": 2
}
```

## Формат ошибок

Ошибки возвращаются в едином JSON-формате.

Пример ошибки валидации:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data",
    "details": {
      "email": "Email is required"
    }
  }
}
```

Пример ошибки, если пользователь не найден:

```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User not found"
  }
}
```

Пример ошибки, если `user-service` недоступен:

```json
{
  "error": {
    "code": "USER_SERVICE_UNAVAILABLE",
    "message": "User service is unavailable"
  }
}
```

## Тестирование

Для запуска тестов:

```bash
pytest
```

Также можно запустить тесты с подробным выводом:

```bash
pytest -v
```

В проекте проверяются:

- создание пользователей;
- получение пользователей;
- валидация данных пользователя;
- создание заказов;
- проверка существования пользователя при создании заказа;
- обработка недоступности `user-service`;
- единый формат ошибок.

## OpenAPI

OpenAPI-спецификация находится в файле:

```text
docs/openapi.yaml
```

Её можно открыть в Swagger Editor или использовать для генерации документации API.

## Postman

Postman-коллекция находится в папке:

```text
postman/
```

Коллекцию можно импортировать в Postman и использовать для ручной проверки API.

## CI

В проект добавлен GitHub Actions workflow:

```text
.github/workflows/ci.yml
```

CI запускает проверку проекта и тесты при push и pull request.

## Что демонстрирует проект

Мой проект показывает навыки:

- разработки REST API на Flask;
- разделения backend-логики на несколько сервисов;
- организации межсервисного взаимодействия;
- обработки ошибок в API;
- валидации входных данных;
- написания автотестов;
- работы с Docker и Docker Compose;
- подготовки документации API.

## Статус проекта

Проект является учебным, но оформлен как портфолио-проект для демонстрации backend-навыков.

