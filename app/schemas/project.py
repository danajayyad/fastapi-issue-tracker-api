from pydantic import BaseModel, ConfigDict
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
    issues_count : int # triggers @hybrid_property (because of model_config) After getting it, it checks if the attribute is int, just like any other one.
    owner_id : int 
    
    model_config = ConfigDict(from_attributes=True)  # pydantic expects a dict, but it recieves a model instance. This allows Pydantic to read input using . (dot-notation) insteade of [] which works on the model instance
    