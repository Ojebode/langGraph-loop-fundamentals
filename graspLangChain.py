""" This code is to understand the LangGraph framework using Python while loop"""

from dotenv import load_dotenv
import os
import json
import re
import logging
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage

filename = __file__.replace("py","log")
logging.basicConfig(filename=filename, level="DEBUG",
                    format='%(asctime)s - %(message)s)',
                    datefmt='')

api_key = os.getenv("OPENAI_KEY")
model = ChatOpenAI(model_name="gpt-4o", openai_api_key=api_key)

messages = [SystemMessage(content="You are a helpful assistant"),
            HumanMessage(content="What is 32 multiplied by 32, then subtract 24 to that result?")]

