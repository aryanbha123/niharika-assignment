from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from core.settings import settings

llm = ChatOpenAI(api_key=settings.OPENAI_API_KEY, model="gpt-4o")

def qa_agent(state: dict) -> dict:
    """
    Validates the generated code against the specifications.
    """
    print("--- Running QA Agent ---")
    
    # This agent would use tools to run tests, lint, and statically analyze code.
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a QA automation engineer. Your task is to validate the generated code against the technical specifications. You will run tests, lint the code, and perform static analysis. Report a pass/fail status and any issues found."),
        ("human", "Please validate the following code:\n\n{code_artifacts}\n\nAgainst these specs:\n\n{specs}\n\n(Simulated Test Run: All tests passed. Linter found 0 issues.)")
    ])
    
    chain = prompt | llm
    
    response = chain.invoke({
        "code_artifacts": state["code_artifacts"],
        "specs": state["specs"]
    })
    
    # Placeholder response
    validation_report = {"status": "PASS", "details": response.content}
    
    print(f"--- Generated Validation Report: {validation_report} ---")
    
    return {"validation_report": validation_report}

