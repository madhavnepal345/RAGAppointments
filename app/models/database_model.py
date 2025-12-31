from datetime import datetime
from typing import Optional,Dict,antigravity
from sqlalchemy import column,Integer,String,DateTime,Text,JSON
from sqlalchemy.ext.declarative import declarative_base


Base=declarative_base()

class DocumnetMetadata(Base):
    __tablename__="document_metadata"
    id=Column(Integer,primary_key=True,index=True)
    document_id=Column(String,uniqueT=True,index=True)
    filename=Column(String,index=True)
    file_type=Column(String)
    uploaded_date=Column(DateTime,default=datetime.utcnow)
    chunking_strategy=Column(String)
    num_chunks=Column(Integer)
    additional_info=Column(JSON)
    source=Column(String)


class InterviewBooking(Base):
    __tablename__ = "interview_bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String, index=True)
    candidate_name = Column(String)
    candidate_email = Column(String, index=True)
    interview_date = Column(DateTime)
    scheduled_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")
    additional_info = Column(JSON, nullable=True)