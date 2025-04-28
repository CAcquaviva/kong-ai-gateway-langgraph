# https://platform.openai.com/docs/api-reference/chat


from typing import TypedDict
from langgraph.graph import StateGraph, START, END




class State(TypedDict):
    messages: str
    model_name: str
    response: str


def node_1(state: dict):
    completions = client.chat.completions.create(
        model=state["model_name"],
        messages=state["messages"]
    )
    return {"response": completions.choices[0].message}

builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)

graph = builder.compile()



from openai import OpenAI
import os
client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)




text = "What's the longitude and latitude of Seattle"
state_dict = {}
state_dict["messages"] = [{"role": "user", "content": text}]
state_dict["model_name"] = "gpt-4"




print(graph.invoke({"messages": state_dict["messages"], "model_name": state_dict["model_name"]}))
