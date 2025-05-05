from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_community.utilities.openweathermap import OpenWeatherMapAPIWrapper
import httpx



@tool
def get_weather(location: str):
    """Call to get the weather from a specific location."""
    print("calling get_weather function")
    openweathermap_url = kong_dp + "/openweathermap-route"
    result = httpx.get(openweathermap_url, params={"q": location})
    return result.json()


@tool
def get_music_concerts(location: str):
    """Call to get the events in a given location."""
    print("calling get_music_concerts function")
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
    return result.json()["events"]["results"][0]["concepts"][0]["label"]["eng"]


@tool
def get_traffic(location: str):
    """Call to get the traffic situation of a given location."""
    print("calling get_traffic function")
    traffic_url = kong_dp + "/tavily-traffic-route"
    data={"query": f"Generally, what is the worst time of day for car traffic in {location}", "search_depth": "advanced"}
    result = httpx.post(traffic_url, json=data)
    return result.json()["results"][0]["content"]


tools = [get_weather, get_music_concerts, get_traffic]
#kong_dp = "http://127.0.0.1"
kong_dp = "http://proxy1.kong"
agent_url = kong_dp + "/agent-route"

client = ChatOpenAI(base_url=agent_url, model="", api_key="dummy", default_headers={"apikey": "123456"})


graph = create_react_agent(client, tools)
