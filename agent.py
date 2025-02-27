from pprint import pprint
from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

prompt = ChatPromptTemplate(
    [
        (
            "system",
            "You are a helpful weather assistant.\
                Always say the name of the user when responding. \
                When responding about the weather, use the provided tool to get the numbers. \
                Assume the temperature is in Farenheits. \
                Also give advice on what to wear in the city.",
        ),
        ("placeholder", "{messages}"),
    ]
)

model = ChatOllama(model="llama3.2:latest", temperature=0.8)


@tool
def get_weather(city: Literal["Round Rock", "Cedar Park"]):
    """Returns the temperature value for the specified city in Farenheits.

    Args:
        city (Literal["Round Rock", "Cedar Park"]): The city to get weather for.
            Must be either "Round Rock" or "Cedar Park".

    Returns:
        str: The weather conditions for the specified city in Farenheits.
    """
    resp = input(f"What's the weather in {city}?")
    return resp


tools = [get_weather]

agent = create_react_agent(model, tools, prompt=prompt)

history = [("user", "My name is Dima")]
query = "What is the weather in Round Rock?"
history.append(("user", query))

inputs = {"messages": history}

resp = agent.stream(inputs, stream_mode="values")

for s in resp:
    message = s["messages"][-1]
    pprint(message.content)
