from pydantic import BaseModel, HttpUrl


class IngestRequest(BaseModel):
    url: HttpUrl