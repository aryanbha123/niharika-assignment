from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from core.settings import settings

llm = ChatOpenAI(api_key=settings.OPENAI_API_KEY, model="gpt-4o")

def lead_engineer_agent(state: dict) -> dict:
    """
    Generates user stories from epics.
    """
    print("--- Running Lead Engineer Agent ---")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert lead engineer. Your task is to break down the provided epics into detailed, actionable user stories from the user's perspective, including acceptance criteria."),
        ("human", "Please break down these epics into user stories:\n\n{epics}")
    ])
    
    chain = prompt | llm
    
    response = chain.invoke({"epics": state["epics"]})
    
    # Placeholder response
    user_stories = [{"story": "User Story 1", "criteria": response.content}]
    
    print(f"--- Generated User Stories: {user_stories} ---")
    
    return {"user_stories": user_stories}