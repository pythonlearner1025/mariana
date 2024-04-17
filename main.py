from dotenv import load_dotenv
from prompt import main_prompt, obs_prompt, sys_prompt
from openai import OpenAI
from tools import *
from agents import OAIAgent, AnthropicAgent, GroqAgent

import argparse
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OAI"))

def run_agent(agent):
    while agent.burn < agent.budget:
        agent.run()
        print(f'in_toks: {agent.latest.input_tokens} | out_toks: {agent.latest.output_tokens} | msg cost: ${agent.get_latest_burn()} | total cost: ${agent.get_burn()}')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", "-q", type=str, required=True, help="The question to ask the research agent.")
    parser.add_argument("--budget", "-b", type=float, required=True, help="The budget for the research agent in dollars.")
    parser.add_argument("--agent", type=str)
    args = parser.parse_args()

    query = args.query
    budget = args.budget
    if args.agent == 'openai':
        agent = OAIAgent(os.getenv("OAI"), main_prompt(query), budget)
    elif args.agent == 'anthropic':
        agent = AnthropicAgent(os.getenv("ANTHROPIC"), main_prompt(query), budget)
    elif args.agent == 'groq':
        agent = GroqAgent(os.getenv("GROQ"), main_prompt(query), budget)

    run_agent(agent)

if __name__ == '__main__':
    main()