from pydantic import BaseModel

class CreateProjectRequest(BaseModel):
    name : str
    
class ProjectRequest(BaseModel):
    id : int