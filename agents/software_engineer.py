from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from core.settings import settings

llm = ChatOpenAI(api_key=settings.OPENAI_API_KEY, model="gpt-4o")

def software_engineer_agent(state: dict) -> dict:
    """
    Generates code from technical specifications.
    """
    print("--- Running Software Engineer Agent ---")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a senior software engineer. Your task is to write clean, efficient, and production-ready Python code based on the provided technical specifications. Adhere to all project conventions and include unit tests."),
        ("human", "Here are the technical specifications:\n\n{specs}\n\nPlease generate the Python code and corresponding unit tests.")
    ])
    
    chain = prompt | llm
    
    response = chain.invoke({"specs": state["specs"]})
    
    # Placeholder response
    code_artifacts = {
        "generated/main.py": f"# Generated Code\n\n{response.content}",
        "generated/test_main.py": f"# Generated Tests\n\n# {response.content}"
    }
    
    # In a real scenario, you'd write these to the filesystem
    print(f"--- Generated Code Artifacts: {code_artifacts.keys()} ---")
    
    return {"code_artifacts": code_artifacts}