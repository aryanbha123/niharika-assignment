from fastapi import FastAPI

# Create a FastAPI app instance
app = FastAPI()


# Define a root endpoint
@app.get("/")
def read_root():
    """
    This is the root endpoint of the API.
    It returns a simple JSON response.
    """
    return {"message": "Hello, World!"}
