from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_community.utilities.openweathermap import OpenWeatherMapAPIWrapper
import httpx



@tool
def get_weather(location: str):
    """Call to get the weather from a specific location."""
    print("starting get_weather function")
    openweathermap_url = kong_dp + "/openweathermap-route"
    result = httpx.get(openweathermap_url, params={"q": location})
    print("finishing get_weather function")
    return result.json()


@tool
def get_music_concert(location: str):
    """Call to get the events in a given location."""
    print("starting get_music_concerts function")
    searchevent_url = kong_dp + "/searchevent-route"
    location = location.replace(" ", "_")
    data={
        "query": {
            "$query": {
                "$and": [
                    {
                        "categoryUri": "dmoz/Arts/Music/Bands_and_Artists"
                    },
                    {
                        "locationUri": f"http://en.wikipedia.org/wiki/{location}"
                    }
                ]
            },
            "$filter": {
                "forceMaxDataTimeWindow": "31"
            }
        },
        "resultType": "events",
        "eventsSortBy": "date",
        "eventImageCount": 1,
        "storyImageCount": 1
    }
    result = httpx.post(searchevent_url, json=data)
    print("finishing get_music_concert function")
    return result.json()["events"]["results"][0]["concepts"][0]["label"]["eng"]


@tool
def get_traffic(location: str):
    """Call to get the traffic situation of a given location."""
    print("starting get_traffic function")
    traffic_url = kong_dp + "/tavily-traffic-route"
    data={"query": f"Generally, what is the worst time of day for car traffic in {location}", "search_depth": "advanced"}
    result = httpx.post(traffic_url, json=data)
    print("finishing get_traffic function")
    return result.json()["results"][0]["content"]


tools = [get_weather, get_music_concert, get_traffic]


kong_dp = "http://127.0.0.1"
agent_url = kong_dp + "/agent-route"

client = ChatOpenAI(base_url=agent_url, model="", api_key="dummy", default_headers={"apikey": "123456"})


graph = create_react_agent(client, tools)
print(graph.get_graph().draw_ascii())




def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()


inputs = {"messages": [("user", "In my next vacation, I'm planning to visit the city where Jimi Hendrix was born? Is there any music concert to see? Also provide weather and traffic information about the city")]}
print_stream(graph.stream(inputs, stream_mode="values"))
