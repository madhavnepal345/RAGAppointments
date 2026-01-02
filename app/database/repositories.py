from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.database_models import DocumentMetadata, InterviewBooking


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_document_metadata(
        self,
        document_id: str,
        filename: str,
        file_type: str,
        chunking_strategy: str,
        num_chunks: int,
        metadata: Optional[Dict[str, Any]] = None
    ) -> DocumentMetadata:
        db_document = DocumentMetadata(
            document_id=document_id,
            filename=filename,
            file_type=file_type,
            chunking_strategy=chunking_strategy,
            num_chunks=num_chunks,
            metadata=metadata or {},
            upload_date=datetime.utcnow()
        )
        self.db.add(db_document)
        self.db.commit()
        self.db.refresh(db_document)
        return db_document
    
    def get_document_by_id(self, document_id: str) -> Optional[DocumentMetadata]:
        return self.db.query(DocumentMetadata)\
            .filter(DocumentMetadata.document_id == document_id)\
            .first()
    
    def list_documents(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[DocumentMetadata]:
        return self.db.query(DocumentMetadata)\
            .order_by(desc(DocumentMetadata.upload_date))\
            .offset(skip)\
            .limit(limit)\
            .all()


class InterviewBookingRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_booking(
        self,
        conversation_id: str,
        candidate_name: str,
        candidate_email: str,
        interview_date: datetime,
        additional_info: Optional[Dict[str, Any]] = None
    ) -> InterviewBooking:
        booking = InterviewBooking(
            conversation_id=conversation_id,
            candidate_name=candidate_name,
            candidate_email=candidate_email,
            interview_date=interview_date,
            additional_info=additional_info or {},
            status="confirmed"
        )
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        return booking
    
    def get_booking_by_conversation_id(
        self,
        conversation_id: str
    ) -> Optional[InterviewBooking]:
        return self.db.query(InterviewBooking)\
            .filter(InterviewBooking.conversation_id == conversation_id)\
            .first()
    
    def get_bookings_by_email(self, email: str) -> List[InterviewBooking]:
        return self.db.query(InterviewBooking)\
            .filter(InterviewBooking.candidate_email == email)\
            .order_by(desc(InterviewBooking.interview_date))\
            .all()