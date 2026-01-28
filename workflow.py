from langgraph.graph import StateGraph, END
from langgraph.checkpoint.aiopostgres import PostgresSaver
from api.schemas import AgentWorkflowState
from agents import (
    product_manager_agent,
    lead_engineer_agent,
    system_architect_agent,
    software_engineer_agent,
    qa_agent
)

# --- State and Routing Logic ---

def anext(state: AgentWorkflowState, next_step: str):
    """Helper to update the 'next_step' in the state."""
    return {"next_step": next_step, "approved": False}

def should_continue(state: AgentWorkflowState) -> str:
    """Router function to determine the next node or wait for approval."""
    if state.get("approved"):
        # If approved, proceed to the next designated step
        return state["next_step"]
    # Otherwise, wait for human-in-the-loop (HIL) approval
    return "waitForApproval"

# --- Graph Definition ---

# 1. Define nodes for each agent
def product_manager_node(state: AgentWorkflowState):
    result = product_manager_agent(state)
    return {**result, **anext(state, "lead_engineer_agent")}

def lead_engineer_node(state: AgentWorkflowState):
    result = lead_engineer_agent(state)
    return {**result, **anext(state, "system_architect_agent")}

def system_architect_node(state: AgentWorkflowState):
    result = system_architect_agent(state)
    return {**result, **anext(state, "software_engineer_agent")}

def software_engineer_node(state: AgentWorkflowState):
    result = software_engineer_agent(state)
    return {**result, **anext(state, "qa_agent")}

def qa_node(state: AgentWorkflowState):
    result = qa_agent(state)
    return {**result, "next_step": "end"}

def wait_for_approval_node(state: AgentWorkflowState):
    """A dummy node that simply waits."""
    print("--- Waiting for approval ---")
    return {}

# 2. Define the workflow graph
workflow = StateGraph(AgentWorkflowState)

workflow.add_node("product_manager_agent", product_manager_node)
workflow.add_node("lead_engineer_agent", lead_engineer_node)
workflow.add_node("system_architect_agent", system_architect_node)
workflow.add_node("software_engineer_agent", software_engineer_node)
workflow.add_node("qa_agent", qa_node)
workflow.add_node("waitForApproval", wait_for_approval_node)

# 3. Define the edges and control flow
workflow.set_entry_point("product_manager_agent")

workflow.add_conditional_edges("product_manager_agent", should_continue)
workflow.add_conditional_edges("lead_engineer_agent", should_continue)
workflow.add_conditional_edges("system_architect_agent", should_continue)
workflow.add_conditional_edges("software_engineer_agent", should_continue)
workflow.add_conditional_edges("qa_agent", lambda s: "end" if s["next_step"] == "end" else "waitForApproval")

# This edge connects the "wait" state back to the router
workflow.add_conditional_edges("waitForApproval", should_continue)

# 4. Compile the graph with checkpointing enabled
memory = PostgresSaver.from_conn_string("postgresql+psycopg://user:password@localhost:5432/mydb")
graph = workflow.compile(checkpointer=memory)
