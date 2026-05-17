from langchain.agents import create_agent
from langchain.tools import tool
from langchain_aws import ChatBedrock

from tools import get_weather


llm = ChatBedrock(
    model_id="amazon.nova-micro-v1:0",
    region_name="us-east-1"
)


@tool
def weather_tool(city: str):
    """Get current weather for a city"""
    return get_weather(city)


agent = create_agent(
    model=llm,
    tools=[weather_tool],
    system_prompt="""
    You are a helpful weather assistant.
    Give concise weather summaries.
    Mention temperature, humidity, and conditions.
    Suggest precautions for extreme weather.
    Recommend Carrying umbrella if conditions is Moderate rain
    """
)


response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is the weather in Hoshiarpur?"
            }
        ]
    }
)

#print(response)
print(response["messages"][-1].content)