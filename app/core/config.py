from typing import Optional,Literal
from pydantic_settings import BaseSettings
from pydantic import Field  

class Settings(BaseSettings):

    #API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "RAG Backend"



#Database 
    DATABASE_URL: Optional[str] = None
    MONGO_URL: Optional[str] = None
    REDIS_URL: str = "redis://localhost:6379"
    
    # Vector Store 
    VECTOR_STORE_TYPE: Literal["pinecone", "qdrant", "weaviate", "milvus"] = "qdrant"


    PINECONE_API_KEY: Optional[str] = None
    PINECONE_ENVIRONMENT: Optional[str] = None
    PINECONE_INDEX: str = "rag-index"
    
    # Qdrant
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION: str = "rag_collection"
    
    # Weaviate
    WEAVIATE_URL: Optional[str] = None
    WEAVIATE_API_KEY: Optional[str] = None
    
    # Milvus
    MILVUS_HOST: str = "localhost"
    MILVUS_PORT: int = 19530


    #Chunking 
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

        
settings = Settings()
