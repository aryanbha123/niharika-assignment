from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from core.settings import settings

# Initialize the language model
llm = ChatOpenAI(api_key=settings.OPENAI_API_KEY, model="gpt-4o")

def product_manager_agent(state: dict) -> dict:
    """
    Generates epics from a product request.
    """
    print("--- Running Product Manager Agent ---")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a world-class product manager. Your task is to take a raw product request and decompose it into a clear, concise set of epics. Focus on the high-level goals and outcomes."),
        ("human", "Please break down this product request into epics:\n\n{product_request}")
    ])
    
    chain = prompt | llm
    
    response = chain.invoke({"product_request": state["product_request"]})
    
    # For now, we'll just use a placeholder.
    # In a real scenario, you would parse the LLM response into a structured format.
    epics = [{"name": "Epic 1", "description": response.content}]
    
    print(f"--- Generated Epics: {epics} ---")
    
    return {"epics": epics}

