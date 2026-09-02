from datetime import datetime
from sqlalchemy.orm import relationship
from app.database.database import Base
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Enum as SQLEnum 
from ..core.enums import Status, Priority
    
class Issues(Base):
    __tablename__ = 'issues'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    description = Column(String)
    priority =  Column(SQLEnum(Priority))
    status = Column(SQLEnum(Status))
    project_id = Column(Integer, ForeignKey("projects.id")) 
      
    project = relationship("Projects", back_populates="issues")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable= False, onupdate=datetime.utcnow)