# Flask Microservices API

**Flask Microservices API** — учебный backend-проект из двух Flask-сервисов: пользователей и заказов.

Проект показывает базовый service-to-service flow: перед созданием заказа `order-service` обращается к `user-service` по HTTP и проверяет существование пользователя. Отдельно обрабатывается ситуация недоступности зависимого сервиса.

## Что демонстрирует проект

- декомпозицию backend на два независимых сервиса;
- REST API на Flask;
- межсервисное HTTP-взаимодействие через Requests;
- валидацию входных данных;
- единый JSON-формат ошибок;
- обработку `user-service` unavailable;
- OpenAPI и Postman;
- Docker Compose;
- pytest;
- GitHub Actions CI.

## Стек

- Python
- Flask
- Requests
- pytest
- Docker / Docker Compose
- OpenAPI
- Postman
- GitHub Actions

## Архитектура

```text
Client
  │
  ├──────────────► user-service
  │                    ▲
  │                    │ HTTP user lookup
  └──────────────► order-service
```

`order-service` не создаёт заказ для неизвестного пользователя и возвращает понятную ошибку, если `user-service` временно недоступен.

## Структура

```text
flask-microservices-api/
├── services/
│   ├── user_service/
│   └── order_service/
├── tests/
├── docs/
├── postman/
├── .github/workflows/ci.yml
├── .env.example
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Локальный запуск

```bash
git clone https://github.com/nikamurkaa/flask-microservices-api.git
cd flask-microservices-api
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
python -m services.user_service.run
```

Во втором терминале:

```powershell
$env:USER_SERVICE_URL="http://127.0.0.1:5001"
python -m services.order_service.run
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements-dev.txt
python -m services.user_service.run
```

Во втором терминале:

```bash
export USER_SERVICE_URL="http://127.0.0.1:5001"
python -m services.order_service.run
```

По умолчанию:

```text
user-service:  http://127.0.0.1:5001
order-service: http://127.0.0.1:5002
```

## Docker Compose

```bash
docker compose up --build
```

## Проверка

```bash
pytest
```

Архитектурные заметки: [`docs/architecture.md`](docs/architecture.md).  
OpenAPI: [`docs/openapi.yaml`](docs/openapi.yaml).  
Postman: [`postman/`](postman/).

## CI

`.github/workflows/ci.yml` запускает автоматические проверки. GitHub Actions workflow проекта запускался успешно.

## Статус

Проект завершён и используется как portfolio case по **Flask, REST API, service-to-service communication, testing и containerization**.

## Автор

[Николь Журбенко](https://github.com/nikamurkaa)
