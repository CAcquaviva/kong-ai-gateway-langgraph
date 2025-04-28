from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
from langchain_community.utilities.openweathermap import OpenWeatherMapAPIWrapper
import httpx



class State(TypedDict):
    """The state of the agent."""
    messages: Annotated[Sequence[BaseMessage], add_messages]


@tool
def get_weather(location: str):
    """Call to get the weather from a specific location."""
    openweathermap_url = kong_dp + "/openweathermap-route"
    result = httpx.get(openweathermap_url, params={"q": location})
    return result.json()


@tool
def get_composer(piece: str):
    """Call to get the composer of a specific piece."""
    deezer_url = kong_dp + "/deezer-route"
    result = httpx.get(deezer_url, params={"q": piece})
    return result.json()["data"][0]["artist"]["name"]


@tool
def get_mathematician(theorem: str):
    """Call to get the mathematician of a specific theorem."""
    wikipedia_url = kong_dp + "/wikipedia-route"
    result = httpx.get(wikipedia_url, params={"srsearch": theorem})
    return result.json()["query"]["search"][0]


tools = [get_weather, get_composer, get_mathematician]



def call_model(state: State):
    system_prompt = SystemMessage(
        "You are a helpful AI assistant, please convert the current San Francisco temperature to Celsius."
    )
    response = client.invoke([system_prompt] + state["messages"])
    return {"messages": [response]}


# Define the conditional edge that determines whether to continue or not
def should_continue(state: State):
    messages = state["messages"]
    last_message = messages[-1]
    # If there is no function call, then we finish
    if not last_message.tool_calls:
        return "end"
    # Otherwise if there is, we continue
    else:
        return "continue"


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()






tools = [get_weather, get_composer, get_mathematician]
tool_node = ToolNode(tools)






builder = StateGraph(State)
builder.add_node("agent_node", call_model)
builder.add_edge(START, "agent_node")
builder.add_node("tool_node", tool_node)
builder.add_edge("tool_node", END)
    
builder.add_conditional_edges(
    # First, we define the start node. We use `agent`.
    # This means these are the edges taken after the `agent` node is called.
    'agent_node',
    # Next, we pass in the function that will determine which node is called next.
    #conditional_edge
    should_continue,
    # Finally we pass in a mapping.
    # The keys are strings, and the values are other nodes.
    # END is a special node marking that the graph should finish.
    # What will happen is we will call `should_continue`, and then the output of that
    # will be matched against the keys in this mapping.
    # Based on which one it matches, that node will then be called.
    {
        # If `tools`, then we call the tool node.
        "continue": "tool_node",
        # Otherwise we finish.
        "end": END,
    },
)

builder.add_edge("tool_node", "agent_node")
graph = builder.compile()

from IPython.display import Image, display
display(Image(graph.get_graph().draw_mermaid_png()))








kong_dp = "http://localhost:80"
agent_url = kong_dp + "/agent-route"

client = ChatOpenAI(base_url=agent_url, model="", api_key="dummy")
client = client.bind_tools(tools)





inputs = {"messages": [("user", "what's the wheater in the city where the author of 'Like a Rolling Stone' was born?")]}
print_stream(graph.stream(inputs, stream_mode="values"))
