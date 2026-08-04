from fastapi import APIRouter, HTTPException
from app.logger import logger
from app.schemas.ingest import IngestRequest
from app.ingestion import IngestionService

router = APIRouter(tags=["Ingestion"])

ingestion_service = IngestionService()


@router.post("/ingest")
async def ingest(request: IngestRequest):

    try:

        result = await ingestion_service.ingest_website(
            str(request.url)
        )

        return {
            "status": "success",
            **result,
        }

    except Exception as e:
        logger.exception("Failed to ingest website")

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )