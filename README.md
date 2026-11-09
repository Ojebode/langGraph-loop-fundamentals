# Simple Agent Loop: Tool-Calling Agent in a Plain Python Loop
A minimal tool-calling AI agent built with a plain Python `while` loop, no agent framework. It shows the **Think → Act → Observe** cycle that frameworks like LangGraph automate.

## How it works

1. **Think**: the full message history is sent to the model (GPT-4o via LangChain).
2. **Act**: if the model requests a tool, the script runs it.
3. **Observe**: the tool result is appended to the history and sent back to the model.
4. The loop repeats until the model replies without requesting a tool. That reply is the final answer.

The `while` loop is the agent harness. It keeps the message history, runs the tools the model requests, and decides when to stop. A `MAX_STEPS` limit stops the loop if the model never finishes.

## Project structure

```
langgraph-loop-fundamentals/
├── agent_loop.py       # The agent: calculator tool, loop, and entry point
├── sample_output.txt   # Example output from one run of the agent
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── .gitignore          # Keeps .env and log files out of Git
```

## Setup

You need Python 3, Git, and an OpenAI API key.

Clone the repository and move into the project folder:

```bash
git clone https://github.com/Ojebode/langgraph-loop-fundamentals.git
cd langgraph-loop-fundamentals
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Then create a file named `.env` in the same folder and add your key:

```
OPENAI_KEY=your-api-key-here
```


## Usage

Run the script and type a question when prompted:

```bash
python agent_loop.py
```

For example, you can enter:
```
What is 32 multiplied by 32, then subtract 24 from the result?
```

The script prints each step of the loop, then the final answer. See `sample_output.txt` for the output of one example run. The wording will vary, but it will look like this:

```
Final Answer: 32 multiplied by 32 is 1024, and subtracting 24 from that result gives you 1000.
```

A detailed log is also written to `agent_loop.log`.

## Limitations

- This is a learning demo, not production code.
- The calculator uses `eval` with input filtering, which is not a true sandbox, so do not expose it to untrusted input.
- The agent has only one tool and no memory between runs.
