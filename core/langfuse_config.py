from langfuse import Langfuse
from langfuse.callback import CallbackHandler
from core.settings import settings

# Initialize Langfuse client
# This can be a singleton instance to be reused across the application
langfuse_client = Langfuse(
    public_key=settings.LANGFUSE_PUBLIC_KEY,
    secret_key=settings.LANGFUSE_SECRET_KEY,
    host=settings.LANGFUSE_HOST,
)

def get_langfuse_callback(thread_id: str):
    """
    Returns a configured Langfuse callback handler for a specific thread.
    """
    return CallbackHandler(
        public_key=settings.LANGFUSE_PUBLIC_KEY,
        secret_key=settings.LANGFUSE_SECRET_KEY,
        host=settings.LANGFUSE_HOST,
        thread_id=thread_id
    )
