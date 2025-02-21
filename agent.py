from pprint import pprint
from typing import Literal

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful weather assistant. When responding about the weather, also give advice on what to weather in the city.",
        ),
        MessagesPlaceholder("messages"),
    ]
)

model = ChatOllama(model="MFDoom/deepseek-r1-tool-calling:14b", temperature=0.8)


@tool
def get_weather(city: Literal["Round Rock", "Cedar Park"]):
    """Returns the weather value for the specified city.

    Args:
        city (Literal["Round Rock", "Cedar Park"]): The city to get weather for.
            Must be either "Round Rock" or "Cedar Park".

    Returns:
        str: The weather conditions for the specified city.
    """
    resp = input(f"What's the weather in {city}?")
    return resp


tools = [get_weather]

agent = create_react_agent(model, tools, prompt=prompt)

inputs = {"messages": [("user", "what is the weather in round rock?")]}

resp = agent.stream(inputs, stream_mode="values")

for s in resp:
    message = s["messages"][-1]
    pprint(message.content)
