# iatlas-backend/models/document.py
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.db import Base
import uuid

class Documnet(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("user_id"), nullable=False)

    filename = Column(String, nullable=True)
    original_text = Column(Text, nullable=True)
    file_size = Column(Integer, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relações
    user = relationship("User")