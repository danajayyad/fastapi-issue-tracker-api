from app.database.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

from app.models.user import Users

class Projects(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key= True)
    name = Column(String, unique=True)
    issues_count = Column(Integer, default=0)
    owner_id = Column(Integer, ForeignKey("users.id"))