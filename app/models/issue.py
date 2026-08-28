from app.database.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Issues(Base):
    __tablename__ = 'issues'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    description = Column(String)
    project_id = Column(Integer, ForeignKey("projects.id")) 