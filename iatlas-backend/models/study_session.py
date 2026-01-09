from sqlalchemy import Column, Nullable, String, Text, Integer, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.db import Base
import uuid

class StudySewsson(Base):
    __tablename__ = "study_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("user_id"), nullable=False, index=True)
    
    # Documento Original
    document_text = Column(Text, nullable=False)
    document_sie = Column(Integer, nullable=True) # bytes

    # Tipo de análise
    analisys_type = Column(String, nullable=False, index=True)# 'resume', 'qa', 'explain'

    kid_mode = Column = Column(Boolean, default=False)
    age_level = Column(Integer, nullable=True) # 6-18

    # Resultados (JSON)
    results = Column(JSON, nullable=False)

    # Tokens
    tokens_used = Column(Integer, default=0)

    # Timestamp
    created_at = Column(DateTime(timezoe=True), server_default=func.now(), index=True)

    user = relationship("User", back_populates="study_sessions")