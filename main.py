from fastapi import FastAPI
from routers import auth, users
from routers import workflow as workflow_router # Import the new workflow router
from routers import projects as projects_router # Import the new projects router
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="Multi-Agent Product Development API",
    description="An API for converting Product Requests to validated code using a multi-agent system.",
    version="1.0.0",
)

# Include existing and new routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(projects_router.router) # Add projects router
app.include_router(workflow_router.router, prefix="/workflow", tags=["Workflow"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Multi-Agent Product Development API"}

