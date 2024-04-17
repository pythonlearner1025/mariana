from dotenv import load_dotenv
from prompt import main_prompt, obs_prompt, sys_prompt
from exa_py import Exa
from openai import OpenAI
from tools import *
from agents import OAIAgent, AnthropicAgent, GroqAgent

import argparse
import os

load_dotenv()

#client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC"),)
client = OpenAI(api_key=os.getenv("OAI"))
exa = Exa(os.getenv("EXA"))

# claude3 costs
in_cost = 15/1000000 # $0.015/1K 
out_cost = 75/1000000 # $0.075/1K

# gpt4 costs
# in: $0.01/1k
# out: $0.03/1k

def run_agent(agent, query):
    while agent.burn < agent.budget:
        agent.call(query)
        print(f'in_toks: {agent.latest.input_tokens} | out_toks: {agent.latest.output_tokens} | msg cost: ${agent.get_latest_burn()} | total cost: ${agent.get_burn()}')
        input()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", "-q", type=str, required=True, help="The question to ask the research agent.")
    parser.add_argument("--budget", "-b", type=float, required=True, help="The budget for the research agent in dollars.")
    args = parser.parse_args()

    query = args.query
    budget = args.budget

    # agent = OAIAgent(os.getenv('OAI'), sys_prompt, budget)
    agent = GroqAgent(os.getenv('GROQ'), sys_prompt, budget)
    run_agent(agent, query)

if __name__ == '__main__':
    main()