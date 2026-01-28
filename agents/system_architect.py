from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from core.settings import settings

llm = ChatOpenAI(api_key=settings.OPENAI_API_KEY, model="gpt-4o")

def system_architect_agent(state: dict) -> dict:
    """
    Generates technical specifications from user stories.
    """
    print("--- Running System Architect Agent ---")
    
    # This agent would use a pgvector tool to search for existing components.
    # For now, we simulate this by just passing the context in the prompt.
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a senior system architect. Your task is to convert user stories into detailed technical specifications. Define data models, API contracts, and system interactions. Search the knowledge base for existing patterns before creating new ones."),
        ("human", "Here are the user stories:\n\n{user_stories}\n\n(Simulated Knowledge Base Search: No existing components found that match the request). Please create the specs.")
    ])
    
    chain = prompt | llm
    
    response = chain.invoke({"user_stories": state["user_stories"]})
    
    # Placeholder response
    specs = [{"spec_name": "API Spec v1", "details": response.content}]
    
    print(f"--- Generated Specs: {specs} ---")
    
    return {"specs": specs}