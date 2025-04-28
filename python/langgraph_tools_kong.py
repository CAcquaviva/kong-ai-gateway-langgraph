from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode


kong_dp = "http://localhost:80"
agent_url = kong_dp + "/agent-route"

client = ChatOpenAI(base_url=agent_url, model="", api_key="dummy")


@tool
def get_weather(location: str):
    """Call to get the weather from a specific location."""
    if any([city in location.lower() for city in ["sf", "san francisco"]]):
        return "It's sunny in San Francisco, but you better look out if you're a Gemini 😈."
    else:
        return f"I am not sure what the weather is in {location}"

@tool
def get_coolest_cities():
    """Get a list of coolest cities"""
    return "nyc, sf"



tools = [get_weather, get_coolest_cities]
client = client.bind_tools(tools)
#client_response = client.invoke("Provide me a list of coolest cities").tool_calls
#client_response = client.invoke("What's the weather in San Francisco?").tool_calls
#print(client_response)







#client_response = client.invoke("Provide me a list of coolest cities")
#client_response = client.invoke("What's the weather in San Francisco?")
client_response = client.invoke("Tell me about Fermat's last theorem")
print(client_response)
print("\n")

tool = ToolNode(tools)
response = tool.invoke({"messages": [client_response]})
print(response)