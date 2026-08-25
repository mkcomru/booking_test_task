# Booking API

REST API для онлайн-бронирования столика.

## Запуск

### Локально

```bash
# установка зависимостей
uv sync

# миграции
uv run alembic upgrade head

# запуск сервера
uv run uvicorn src.main:app --reload --port 8000

# запуск тестов
uv run pytest tests/ -v
```

Или через Justfile:

```bash
just run      # сервер
just test     # тесты
```

### Docker

```bash
docker compose up --build
```

Сервер будет доступен на `http://localhost:8000`. Swagger: `http://localhost:8000/docs`.

## Решения

- **Слоистая архитектура**: роуты / сервис / репозиторий / схемы / модели. Каждый слой отвечает за своё: роуты — HTTP, сервис — бизнес-логика, репозиторий — запросы к БД.
- **Async SQLAlchemy 2.0 + Alembic**: асинхронный доступ к SQLite через aiosqlite. Alembic для миграций — полезная привычка даже для маленького проекта.
- **Pydantic v2 с кастомными валидаторами**: валидация телефона, даты и слотов вынесена в `field_validator` — единое место, работает и на уровне схем, и на уровне API.
- **Service layer с исключениями**: бизнес-ошибки (`BookingNotFoundError`, `SlotAlreadyBookedError`) пробрасываются через исключения, а не через HTTP-коды в сервисе — это позволяет переиспользовать логику.
- **In-memory БД для тестов**: тесты используют `sqlite+aiosqlite:///:memory:` с пересозданием таблиц на каждый тест — быстро и изолированно.

## Что осталось доделать

- Пагинация списка броней (`offset` / `limit`)
- Rate limiting на создание броней
- Поиск брони по телефону
- CI/CD: GitHub Actions с запуском тестов и линтера
