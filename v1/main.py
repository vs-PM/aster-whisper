from fastapi import FastAPI
from .whisper.routes import router as whisper_router
from .docx.routes import router as docx_router


app = FastAPI(
    title="PM_work v1",
    description="API для работы с docx-документами и транскрипцией аудио через Whisper.",
    version="1.0.0",
    contact={
        "name": "PM_work API Support",
        "email": "support@example.com"
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.include_router(whisper_router)
app.include_router(docx_router)


@app.get("/")
def root():
    return {"message": "PM_work v1 API"}
