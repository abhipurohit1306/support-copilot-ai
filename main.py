from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.logger import logger

from app.routes.chat import router as chat_router
from app.routes.ingest import router as ingest_router
from app.routes.health import router as health_router


app = FastAPI(
    title="Support Copilot AI",
    version="1.0.0",
    description="AI-powered RAG Support Copilot",
)


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception(
        "Unhandled application error: %s %s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal server error occurred. Please try again later."
        },
    )


app.include_router(chat_router)
app.include_router(ingest_router)
app.include_router(health_router)