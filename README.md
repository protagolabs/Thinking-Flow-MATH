# Thinking-Flow-MATH

## Introduction 

We are a team of Netmind.AI, our website is also [Netmind.AI](netmind.ai)

This repository store the netmindai competition project in the AAAI2024 COMPETITION ON MATH PROBLEM SOLVING - TRACK2 leaderboard.

## Using guidance:

Step 1: Prepare the enviroment:

```bash
git clone https://github.com/protagolabs/Thinking-Flow-MATH
cd Thinking-Flow-MATH 
pip install -r requirements.txt
```

Step 2: Set your own OpenAI-Key

You should follow the OpenAI website to set the OpenAI-Key, before you using any code from this repository.

If you just want to get all the answer from this project. Before you run the `solving_competition.sh`, please complete the openai-key in `scripts/solve_competition.py` line: 12-13

Step 3: Run the script to ght all the answer from this competition:

```bash 
cd Thinking-Flow-Math 
bash solving_competition.sh
```

## Some Using example:

### You want to using this repo in jupyter:

See the notebook: `Thinking-Flow-MATH/scripts/solve_math_question.ipynb`

### For the no-coding using:

(TODO)
We also build a webapp demo by streamlit: `Thinking-Flow-MATH/streamlit_webapp/thinking_flow_netmindai.py`

## Explain for this project

### Multi-Agents System for MATH-SOP (Thinking-FLow)

(We also have a paper(under reviewing now) for this Thinking-FLow. But the prompts in this paper is old version. If you want to know more detail about this project, please read this paper.)
We construct a multi-agent system using a large language model-based agent. The agent system includes:

1. Plan—Agent
2. Solving-Agent
3. MathCoding-Agent
4. Summary-Agent
5. Evaluate-Agent

And for 1-4, we also have another correction-version for each agents.

External tool, Retrieval-Module:
The description: 






