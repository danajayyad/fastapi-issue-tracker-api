from typing import Optional
from pydantic import BaseModel
from ..core.enums import Status, Priority

class CreateIssueRequest(BaseModel):
    title :str
    description :str
    status : Status = Status.OPEN
    priority : Priority = Priority.LOW
    
class UpdateIssueRequest(BaseModel):
    status : Status | None = None
    priority : Priority | None = None
    title : Optional[str] = None # same as str | None = None
    description :str | None = None