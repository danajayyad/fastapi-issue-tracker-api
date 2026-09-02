from pydantic import BaseModel
from ..core.enums import Status, Priority

class CreateProjectRequest(BaseModel):
    name : str # no default manditory
    description: str | None = None
    status : Status = Status.OPEN
    priority : Priority = Priority.LOW

    
    
    
    
class UpdateProjectRequest(BaseModel):
    name : str  | None = None
    description: str | None = None
    status : Status | None = None
    priority : Priority | None = None
    


class ProjectResponse(BaseModel):
    name : str 
    description : str 
    status : Status
    priority : Priority 
    issues_count : int
    owner : str 
    