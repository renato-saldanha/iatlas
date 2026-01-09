from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.db import Base
import uuid

class User(Base):
    __tablename__ = "Users"

    id = Column(String, primary_key=True, defailt=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=True)
    full_name = Column(String, nunllable=True)
    is_active = Column(Boolean, default=True)
    auth_provider = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relações
    study_sessions = relationship("StudySession", back_populates="user")