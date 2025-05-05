from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    messages: str
    response: str


def node_1(state: State) -> State:
    completions = client.chat.completions.create(
        model="gpt-4",
        messages=state["messages"]
    )
    return {"response": completions.choices[0].message.content}


builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)

graph = builder.compile()
print(graph.get_graph().draw_ascii())


from openai import OpenAI
import os
client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)


text = "What's the longitude and latitude of Seattle"
state = {"messages": [{"role": "user", "content": text}], "response": ""}

print("State before invoking the graph")
print(state)
print("-----\n")

print("Invoking the graph")
state = graph.invoke(state)
print("-----\n")

print("State after invoking the graph")
print(state)
print("-----\n")
