from pydantic import BaseModel, validator
from typing import TypedDict, List, Literal, Optional, Dict
import uuid

class UserCreate(BaseModel):
    username: str
    password: str

    @validator('username')
    def username_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Username must not be empty')
        return v

    @validator('password')
    def password_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Password must not be empty')
        return v

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

# --- Schemas for Projects ---

class ProjectCreate(BaseModel):
    name: str

class ProjectOut(BaseModel):
    id: uuid.UUID
    name: str
    owner_id: int

    class Config:
        orm_mode = True


# --- Schemas for Agentic Workflow ---

class RequestInput(BaseModel):
    """Schema for the initial product request."""
    request: str

class AgentWorkflowState(TypedDict):
    """
    Defines the structure of the state that flows through the agent graph.
    """
    product_request: str
    epics: Optional[List[dict]]
    user_stories: Optional[List[dict]]
    specs: Optional[List[dict]]
    code_artifacts: Optional[Dict[str, str]]
    validation_report: Optional[dict]
    
    # Tracking properties
    next_step: str
    approved: bool
