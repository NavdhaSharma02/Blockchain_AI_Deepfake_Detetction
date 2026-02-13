"""
Database models and setup
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class VerificationRecord(Base):
    """Model for storing verification history"""
    __tablename__ = "verification_records"
    
    id = Column(Integer, primary_key=True, index=True)
    media_hash = Column(String, unique=True, index=True, nullable=False)
    file_name = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    
    # Blockchain verification
    blockchain_verified = Column(Boolean, default=False)
    blockchain_uploader = Column(String, nullable=True)
    blockchain_timestamp = Column(Integer, nullable=True)
    
    # AI detection results
    ai_classification = Column(String, nullable=True)
    ai_confidence = Column(Float, nullable=True)
    fake_probability = Column(Float, nullable=True)
    real_probability = Column(Float, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String, nullable=True)
    
    def to_dict(self):
        """Convert record to dictionary"""
        return {
            "id": self.id,
            "media_hash": self.media_hash,
            "file_name": self.file_name,
            "file_type": self.file_type,
            "blockchain_verified": self.blockchain_verified,
            "blockchain_uploader": self.blockchain_uploader,
            "blockchain_timestamp": self.blockchain_timestamp,
            "ai_classification": self.ai_classification,
            "ai_confidence": self.ai_confidence,
            "fake_probability": self.fake_probability,
            "real_probability": self.real_probability,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./verification.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
