from fastapi import APIRouter, HTTPException
import traceback
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
        traceback.print_exc() 

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )