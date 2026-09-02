from app.database.database import db_dependency
from app.dependencies.auth import user_dependency
from fastapi import APIRouter, HTTPException, Path
from starlette import status
from app.models.issue import Issues
from app.models.project import Projects
from app.schemas.issue import CreateIssueRequest, UpdateIssueRequest


router = APIRouter(tags=['issues'])


@router.get('/projects/{project_id}/issues')
async def get_project_issues(db:db_dependency, current_user: user_dependency, project_id : int = Path(gt=0)):
    project = db.quesry(Projects).filter(Projects.id == project_id, Projects.owner_id  == current_user.id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Project with ID {project_id} not found.")
    issues  = db.query(Issues).filter(Issues.project_id == project_id).all()
    return issues


@router.post('/projects/{project_id}/issues')
async def create_issue(db:db_dependency, current_user: user_dependency, create_issue_request: CreateIssueRequest, project_id: int = Path(gt=0)):
    project = db.query(Projects).filter(Projects.owner_id == current_user.id , Projects.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Project with ID {project_id} not found")
    issue = Issues(**create_issue_request.model_dump(), project_id=project_id)
    db.add(issue)
    db.commit()
    db.refresh(issue)
    return issue
    


@router.get('/issues/{issue_id}')
async def get_issue_by_id(db : db_dependency, current_user:user_dependency, issue_id: int = Path(gt=0)):
    issue = db.query(Issues).join(Projects).filter(Projects.owner_id == current_user.id , Issues.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Issue with ID {issue_id} not found.")
    return issue


@router.delete('/issue/{issue_id}')
async def delete_issue_by_id(db:db_dependency, current_user: user_dependency, issue_id : int = Path(gt=0)):
    issue = db.query(Issues).join(Projects).filter(Projects.owner_id ==  current_user.id , Issues.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Issue with ID {issue_id} not found.")
    db.delete(issue)
    db.commit()



# patch beacause changing all the features is optional, put is used when replacing the entire object
@router.patch('/issues/{issue_id}')
async def update_issue(db:db_dependency, current_user: user_dependency, issue_update : UpdateIssueRequest, issue_id: int = Path(gt=0)):
    issue = db.query(Issues).join(Projects).filter(Projects.owner_id == current_user.id, Issues.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Issue with ID {issue_id} not found.")
    update_data = issue_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(issue, key, value) # changing on the tracked row
    db.commit()
    db.refresh(issue)
    return issue
    
    