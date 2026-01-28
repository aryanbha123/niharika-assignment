from fastapi import APIRouter, Depends, HTTPException
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
from api.schemas import ProjectCreate, ProjectOut, UserOut
from api.auth import get_current_user
from api.db import get_db_connection

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=ProjectOut)
def create_project(
    project: ProjectCreate, 
    current_user: UserOut = Depends(get_current_user),
    conn: psycopg2.extensions.connection = Depends(get_db_connection)
):
    """
    Create a new project for the authenticated user.
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        try:
            cur.execute(
                "INSERT INTO projects (name, owner_id) VALUES (%s, %s) RETURNING id, name, owner_id",
                (project.name, current_user['id'])
            )
            new_project = cur.fetchone()
            conn.commit()
            return new_project
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to create project: {e}")

@router.get("/", response_model=List[ProjectOut])
def list_my_projects(
    current_user: UserOut = Depends(get_current_user),
    conn: psycopg2.extensions.connection = Depends(get_db_connection)
):
    """
    List all projects owned by the authenticated user.
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT id, name, owner_id FROM projects WHERE owner_id = %s", (current_user['id'],))
        projects = cur.fetchall()
        return projects
