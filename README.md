
# PM_work v1

## Описание

Микросервисное FastAPI-приложение для работы с docx-документами и транскрипцией аудио через Whisper.

- **/docx/** — генерация docx-файлов по шаблону с подстановкой данных из БД.
- **/whisper/** — транскрипция аудиофайлов (WAV) в текст с помощью Whisper.

## Быстрый старт

1. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Настройте переменные окружения:**
   - Для docx: путь к шаблону (`DOCX_TEMPLATE_PATH`)
   - Для БД: параметры подключения (см. config.py)
3. **Запустите сервер:**
   ```bash
   uvicorn pm_work.v1.main:app --reload
   ```
4. **Swagger UI:**
   - [http://localhost:8000/docs](http://localhost:8000/docs)
   - [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Структура проекта

```
pm_work/
├── v1/
│   ├── main.py           # Точка входа FastAPI
│   ├── docx/             # Логика docx
│   └── whisper/          # Логика whisper
│   └── db/               # Модели и DAO
│   └── tests/            # Тесты
├── requirements.txt
└── README.md
```

## Тестирование

```bash
pytest v1/tests
```

## Примеры запросов

### Генерация docx
```http
POST /docx/generate
{
  "id": 1,
  "values": {"name": "Иван"}
}
```

### Транскрипция аудио
```http
POST /whisper/transcribe
Content-Type: multipart/form-data
file: <WAV-файл>
```

## Контакты

- Поддержка: support@example.com
