"""The week-4 cost estimator, rebuilt as a LangGraph graph."""
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

import cost_tools

tools = [
    tool(cost_tools.lookup_price),
    tool(cost_tools.sum_costs),
    tool(cost_tools.convert_currency),
]
model = ChatOllama(model="qwen3:8b", temperature=0).bind_tools(tools)


def call_model(state: MessagesState):
    """Graph node: ask the model what to do next."""
    return {"messages": [model.invoke(state["messages"])]}


builder = StateGraph(MessagesState)
builder.add_node("model", call_model)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "model")
builder.add_conditional_edges("model", tools_condition)  # tool call? go to "tools", else end
builder.add_edge("tools", "model")
graph = builder.compile()

if __name__ == "__main__":
    question = "Estimate the monthly cost of 3 medium VMs and a medium Postgres database, in CUR."
    result = graph.invoke({"messages": [("user", question)]}, {"recursion_limit": 10})
    for message in result["messages"]:
        message.pretty_print()
    print(graph.get_graph().draw_mermaid())