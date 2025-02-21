from langchain_ollama import ChatOllama

llm1 = ChatOllama(model="deepseek-r1:14b-qwen-distill-q8_0", temperature=0.8)

prompt1 = """
Your goal is to understand the problem related to the exception provided below, the reason for it and suggest the resolution steps:
---
org.apache.kafka.common.config.ConfigException: topic.regex.list cannot be empty when the connector runs in GENERIC mode.
"""

msg = llm1.invoke(prompt1)
print(msg.content)
