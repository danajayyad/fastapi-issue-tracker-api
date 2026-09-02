from datetime import datetime
from ..database.database import Base
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from ..core.enums import Status, Priority


class Projects(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key= True)
    name = Column(String, unique=True, nullable=False)
    description  = Column(Text, nullable=True)
    status = Column(SQLEnum(Status), nullable=False)
    priority = Column(SQLEnum( Priority))
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("Users", back_populates="projects")
    issues = relationship("Issues", back_populates="project", cascade="all, delete-orphan")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)