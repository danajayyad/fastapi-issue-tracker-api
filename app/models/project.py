from datetime import datetime

from app.models.issue import Issues
from ..database.database import Base
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Text, Enum as SQLEnum, select, func
from sqlalchemy.orm import relationship
from ..core.enums import Status, Priority
from sqlalchemy.ext.hybrid import hybrid_property

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
    
    # Used by SQLAlchemy when accessing a loaded object (python attribute). Pydantic reads this seamlessly during serialization.
    @hybrid_property 
    def issues_count(self):
        return len(self.issues)
    
    
    # Used by SQLAlchemy to build a SQL subquery whenever this property is used inside a database query like .filter() or .order_by()
    @issues_count.expression
    def issues_count(cls): # class method
        return (
            select(func.count(Issues.id))
            .where(Issues.project_id == cls.id)
            .correlate_attrs(cls.id)
            .scalar_subquery()
        )
    
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)