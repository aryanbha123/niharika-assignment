import uuid
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from langgraph.errors import GraphNotYetStarted

from api.schemas import RequestInput, AgentWorkflowState, UserOut, ProjectOut
from api.auth import get_current_user
from api.db import get_db_connection
from workflow import graph
from core.langfuse_config import get_langfuse_callback

router = APIRouter(
    tags=["Workflow"]
)

async def check_project_ownership(project_id: uuid.UUID, current_user: UserOut = Depends(get_current_user), conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT owner_id FROM projects WHERE id = %s", (str(project_id),))
        project = cur.fetchone()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        if project['owner_id'] != current_user['id']:
            raise HTTPException(status_code=403, detail="User does not have access to this project")
    return project

@router.post("/projects/{project_id}/workflow", summary="Start a new workflow in a project")
async def start_workflow(
    project_id: uuid.UUID,
    request: str = Form(...),
    document: Optional[UploadFile] = File(None),
    project_owner: dict = Depends(check_project_ownership),
    current_user: UserOut = Depends(get_current_user)
):
    """
    Starts a new agentic workflow run within a specific project.
    """
    thread_id = str(uuid.uuid4())
    config = {
        "configurable": {
            "thread_id": thread_id,
            "thread_metadata": {
                "project_id": str(project_id),
                "user_id": current_user['id']
            }
        },
        "callbacks": [get_langfuse_callback(thread_id)],
    }
    
    # Handle file upload
    document_info = None
    if document:
        # In a real system, you would save this to S3/GCS and pass the URI
        document_info = {"filename": document.filename, "content_type": document.content_type}

    initial_state = {
        "product_request": request, 
        "next_step": "product_manager_agent",
        "document": document_info,
    }

    try:
        # Start the graph execution asynchronously
        await graph.astream(initial_state, config=config)
        return {"thread_id": thread_id, "project_id": project_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start workflow: {str(e)}")


@router.post("/workflow/{thread_id}/approve", summary="Approve the current step")
async def approve_step(thread_id: str, current_user: UserOut = Depends(get_current_user)):
    """
    Approves the last completed step, allowing the workflow to continue.
    (Note: In a real system, you would verify the user has rights to this thread)
    """
    config = {
        "configurable": {"thread_id": thread_id},
        "callbacks": [get_langfuse_callback(thread_id)],
    }

    try:
        await graph.aget_state(config)
    except GraphNotYetStarted:
        raise HTTPException(status_code=404, detail="Workflow not found.")
    
    await graph.aupdate_state(config, {"approved": True})
    
    try:
        await graph.astream(None, config=config)
        return {"status": "approved", "thread_id": thread_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to continue workflow: {str(e)}")


@router.get("/workflow/{thread_id}/status", response_model=AgentWorkflowState, summary="Get workflow status")
async def get_workflow_status(thread_id: str, current_user: UserOut = Depends(get_current_user)):
    """
    Retrieves the current state of the workflow.
    (Note: In a real system, you would verify the user has rights to this thread)
    """
    config = {"configurable": {"thread_id": thread_id}}
    try:
        state = await graph.aget_state(config)
        return state.values
    except GraphNotYetStarted:
        raise HTTPException(status_code=404, detail="Workflow not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting workflow state: {str(e)}")
