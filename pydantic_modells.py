from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
import os


class ModelName(str, Enum):
    HUGGING_FACE = "Huggingface model"

class QueryInput(BaseModel):
    question: str
    session_id: str
    model:ModelName = Field(default=ModelName.HUGGING_FACE)

class QueryResponse(BaseModel):
    answer: str
    session_id: str
    model: ModelName

class DocumentInfo(BaseModel):
    id: int
    filename: str
    upload_timestamp: datetime
    file_size: int
    content_type: str

class DeleteRequest(BaseModel):
    file_id: int