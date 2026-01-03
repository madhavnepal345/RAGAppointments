from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from app.core.database import get_db
from app.services.ingestion import DocumentIngestionService
from app.database.repositories import DocumentRepository
from app.models.schemas import (
    DocumentUpload,
    DocumentResponse,
    HealthCheck
)

router = APIRouter()


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    chunking_strategy: str = Form("recursive"),
    metadata: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    if not (file.filename.endswith('.pdf') or file.filename.endswith('.txt')):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported")
    
    try:
        # Read file content
        content = await file.read()
        
        # Parse metadata
        metadata_dict = json.loads(metadata) if metadata else {}
        
        # Process document
        ingestion_service = DocumentIngestionService()
        result = ingestion_service.process_document(
            file_content=content,
            filename=file.filename,
            chunking_strategy=chunking_strategy,
            metadata=metadata_dict
        )
        
        # Save metadata to database
        repo = DocumentRepository(db)
        db_document = repo.create_document_metadata(
            document_id=result["document_id"],
            filename=result["filename"],
            file_type=result["file_type"],
            chunking_strategy=result["chunking_strategy"],
            num_chunks=result["num_chunks"],
            metadata=result["metadata"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
    
    return DocumentResponse(
        document_id=db_document.document)