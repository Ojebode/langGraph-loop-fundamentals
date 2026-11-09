"""Minimal tool-calling agent built with a plain Python while loop. Purpose: show the Think -> Act -> Observe cycle that frameworks like LangGraph automate.
The model decides whether to call a tool, we run it, feed the result back, and repeat until the model gives a final answer."""

import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

load_dotenv()  # load OPENAI API key from a local .env file

MAX_STEPS = 10  # Safety limit so the loop cannot run forever

filename = Path(__file__).with_suffix(".log")
logging.basicConfig(filename=filename, level="WARNING",
                    format='%(asctime)s - %(message)s')


@tool
def calculator(expression: str):
    """Evaluates a basic arithmetic expression and returns the result.
    Use this for any math, such as addition, subtraction, multiplication,
    or division. Input should be a valid arithmetic expression as a string,
    e.g. '2 + 2' or '15.5 * 3'.
    """
    # The docstring above is sent to the model so it knows when and how to use this tool.
    try:
        # Demo only: restricting builtins is not a real sandbox. Do not expose to untrusted input.
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        logging.exception("Calculator failed")
        return f"Error: {e}"  # Returned to the model to see what went wrong


def run_agent(user_prompt: str):
    api_key = os.getenv("OPENAI_KEY")
    model = ChatOpenAI(model_name="gpt-4o", openai_api_key=api_key)

    # The message list is the agent's entire state; every step appends to it.
    messages = [SystemMessage(content="You are a helpful assistant"),
                HumanMessage(content=user_prompt)]

    # Maps the tool name the model asks for to the actual Python tool
    tool_inventory = {
        "calculator": calculator
    }

    # Tell the model which tools exist (name, description, arguments)
    model_with_tools = model.bind_tools([calculator])

    step = 0
    while True:
        step += 1
        if step > MAX_STEPS:
            return "Stopped: step limit reached without a final answer."

        print(f"\n++++++++++++++++-STEP {step}: INVOKING MODEL-++++++++++++++++\n")
        # THINK: send the full history to the model
        response = model_with_tools.invoke(messages)
        print(json.dumps(response.model_dump(), indent=4, default=str))
        messages.append(response)

        # No tool requested means the model has produced its final answer
        if not response.tool_calls:
            break

        print(f"\n++++++++++++++++-STEP {step}: RUNNING TOOLS-++++++++++++++++\n")
        # ACT: run each tool the model requested
        for call in response.tool_calls:
            if call["name"] in tool_inventory:
                output = tool_inventory[call["name"]].invoke(call["args"])
            else:
                output = f"Unknown tool: {call['name']}"
            # OBSERVE: append the result, linked to the request by tool_call_id,
            # so the model can match each result to the call it made
            messages.append(ToolMessage(content=str(output), tool_call_id=call["id"]))
            print(output)
    # print("**********************-TOTAL MESSAGES-**************************** - ", len(messages))
    # print(json.dumps([message.model_dump() for message in messages], indent=4))
    return messages[-1].content # The model's final answer


def main():
    if not os.getenv("OPENAI_KEY"):
        raise SystemExit("OPENAI_KEY is not set. Add your key to .env")
    prompt = input("Prompt (e.g. 'What is 32 multiplied by 32, then subtract 24 from the result?'): ")
    print("\nFinal Answer:", run_agent(prompt))


if __name__ == "__main__":
    main()


