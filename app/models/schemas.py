from datetime import datetime
from typing import Optional,Dict,Any,Literal,List
from pydantic import BaseModel,Field,EmailStr



class DocumentUpload(Basemodel):
    chunking_strategy:Literal['recursive','semantic']=Field(
        default="recursive",
        description="chunking strategy to be used for document processing"
    )
    metadata:Optional[Dict[str,Any]]=Field(default_factory=dict)

class ChunkingConfig(BaseModel):
    chunk_size:int=Field(default=1000,le=5000)
    chunk_overlap:int=Field(default=200,ge=0, le=1000)


class DocumentResponse(BaseModel):
    document_id:str
    filename:str
    file_type:str
    uploaded_date:datetime
    chunking_strategy:str
    num_chunks:int
    metadata:Dict[str,Any]


#Schema of RAG

class ConversationMessage(BaseModel):
    role:Literal["user","assistant"]
    content:str
    timestamp:datetime=Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    conversation_id:Optional[str]=Field(
        default=None,
        description="Existing conversation ID"
        )
    query:str=Field(...,min_length=1)
    use_rag:bool=Field(default=True)
    top_k:int=Field(default=5,ge=1,le=20)

class ChatResponse(BaseModel):
    conversation_id: str
    answer: str
    sources: List[Dict[str, Any]] = Field(default_factory=list)
    requires_booking: bool = Field(default=False)
    booking_intent: Optional[str] = None


class InterviewBookingRequest(BaseModel):
    conversation_id: str
    candidate_name: str
    candidate_email: EmailStr
    interview_date: datetime
    timezone: str = Field(default="UTC")
    additional_notes: Optional[str] = None


class InterviewBookingResponse(BaseModel):
    booking_id: str
    conversation_id: str
    candidate_name: str
    candidate_email: EmailStr
    interview_date: datetime
    status: str
    scheduled_at: datetime