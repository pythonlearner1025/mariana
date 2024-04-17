import os
import uuid
from datetime import datetime

from openai import OpenAI
from anthropic import Anthropic
from groq import Groq
from tools import execute_tool
from prompt import obs_prompt
import openai
import anthropic
import json
import tiktoken

class Usage:
    def __init__(self):
        self.input_tokens = 0
        self.output_tokens = 0

class BaseAgent:
    def __init__(self):
        self.run_id = str(uuid.uuid4())
        self.log_file = f"logs/{self.run_id}.log"
        dir = os.path.dirname(self.log_file)
        if not os.path.exists(dir): 
            os.mkdir(dir)
        self.log(f"Run ID: {self.run_id}")
        self.log(f"Date: {datetime.now()}")
        print()

    def log(self, text):
        with open(self.log_file, "a") as f:
            f.write(text)
            print(text, end='')

class OAIAgent(BaseAgent):
    def __init__(self, key, sys_prompt, budget, model='gpt-4-turbo-2024-04-09'):
        super().__init__()
        self.tools = json.loads(open('tools/openai_tools.json').read())
        self.client = OpenAI(api_key=key)
        self.assistant = None
        self.budget = budget
        self.burn = 0
        self.in_price = 10/1000000
        self.out_price = 30/1000000
        self.messages = []
        self.model = model 
        self.latest = Usage()
        self.assistant = self.client.beta.assistants.create(
            instructions=sys_prompt,
            model=self.model,
            tools=self.tools
        )
        self.messages = [{'role': 'user', 'content': sys_prompt}]
    
    def run(self):
        self.thread = self.client.beta.threads.create(messages=self.messages)
        input_tokens = count_tok(self.messages[-1]['content'])
        output_tokens = 0
        with self.client.beta.threads.runs.stream(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
        ) as stream:
            for event in stream:
                if isinstance(event, openai.types.beta.assistant_stream_event.ThreadRunStepDelta):
                    txt = event.data.delta.step_details.tool_calls[0].function.arguments
                    output_tokens += count_tok(txt)
                    self.log(txt)
                elif isinstance(event, openai.types.beta.assistant_stream_event.ThreadMessageDelta):
                    txt = event.data.delta.content[0].text.value
                    output_tokens += count_tok(txt)
                    self.log(txt)
                elif isinstance(event, openai.types.beta.assistant_stream_event.ThreadRunRequiresAction):
                    req = event.data.required_action
                    tool_calls = req.submit_tool_outputs.tool_calls
                    outs = []
                    for tool in tool_calls:
                        call_id = tool.id
                        function = tool.function.name
                        output_tokens += count_tok(tool.function.arguments)
                        output_tokens += count_tok(tool.function.name)
                        args = json.loads(tool.function.arguments)
                        self.log('== calling tool ==')
                        self.log(f"{function} {args}")
                        output = execute_tool(function, args)
                        outs.append({'tool_call_id': call_id, 'output': f'{output}'})
                    self.submit_to_run(event, outs)

        self.latest.input_tokens = input_tokens
        self.latest.output_tokens = output_tokens

    def submit_to_run(self, event, outs):
        input_tokens = self.latest.output_tokens
        output_tokens = 0
        with self.client.beta.threads.runs.submit_tool_outputs_stream(
            thread_id=self.thread.id,
            run_id=event.data.id,
            tool_outputs=outs 
        ) as stream:
            for event in stream:
                if isinstance(event, openai.types.beta.assistant_stream_event.ThreadRunStepDelta):
                    txt = event.data.delta.step_details.tool_calls[0].function.arguments
                    output_tokens += count_tok(txt)
                    self.log(txt)
                elif isinstance(event, openai.types.beta.assistant_stream_event.ThreadMessageDelta):
                    txt = event.data.delta.content[0].text.value
                    output_tokens += count_tok(txt)
                    self.log(txt)
                elif isinstance(event, openai.types.beta.assistant_stream_event.ThreadRunRequiresAction):
                    self.log(str(event))
                    req = event.data.required_action
                    tool_calls = req.submit_tool_outputs.tool_calls
                    outs = []
                    for tool in tool_calls:
                        call_id = tool.id
                        function = tool.function.name
                        output_tokens += count_tok(tool.function.arguments)
                        output_tokens += count_tok(tool.function.name)
                        args = json.loads(tool.function.arguments)
                        self.log('== calling tool ==')
                        self.log(f"tool name: {function} ")
                        self.log(f'tool args: {args}')
                        output = execute_tool(function, args)
                        self.log(f'tool output: {output}')
                        outs.append({'tool_call_id': call_id, 'output': f'{output}'})  
                    self.submit_to_run(event, outs)

        self.latest.input_tokens = input_tokens
        self.latest.output_tokens = output_tokens
        self.burn += self.get_latest_burn()
    
    def get_latest_burn(self):
        return self.in_price * self.latest.input_tokens + self.out_price * self.latest.output_tokens
        
    def get_burn(self): 
        return self.burn

class AnthropicAgent(BaseAgent):
    def __init__(self, key, sys_prompt, budget, model='claude-3-opus-20240229'):
        super().__init__()
        self.client = Anthropic(api_key=key)
        self.tools = json.loads(open('tools/anthropic_tools.json').read())
        self.budget = budget
        self.burn = 0
        self.in_price = 15/1000000
        self.out_price = 75/1000000
        self.messages = [{'role': 'user', 'content': sys_prompt}]
        self.model = model
        self.latest = Usage()
    
    def run(self):
        message = self.client.beta.tools.messages.create(
            max_tokens=4096,
            messages=self.messages,
            tools=self.tools,
            model=self.model
        ) 

        cost = self.in_price * message.usage.input_tokens + self.out_price * message.usage.output_tokens
        self.burn += cost
        obs = self.handle_tool(message.content)
        self.messages.append({"role": "user", "content": obs_prompt(obs)})
        self.run()
    
    def handle_tool(self, msgs):
        obs = []
        for msg in msgs:
            if type(msg) == anthropic.types.text_block.TextBlock:  
                self.messages.append({"role": "assistant", "content": msg.text})
                self.log(msg.text)
            elif type(msg) == anthropic.types.beta.tools.tool_use_block.ToolUseBlock:
                tool = msg
                self.log('== calling function ==')
                self.log(f'tool name: {tool.name}')
                self.log(f'tool args {tool.input}')
                result = execute_tool(tool.name, tool.input)
                self.log(f'tool output: {result}')
                obs.append({"tool_name": tool.name, "tool_input": tool.input, "tool_result": result})
        return obs

    def get_latest_burn(self):
        return self.in_price * self.latest.input_tokens + self.out_price * self.latest.output_tokens
        
    def get_burn(self): 
        return self.burn

class GroqAgent(BaseAgent):
    def __init__(self, key, sys_prompt, budget, model='mixtral-8x7b-32768'):
        super().__init__()
        self.client = Groq(api_key=key)
        self.model = model
        self.messages = [{'role': 'user', 'content': sys_prompt}]
        self.budget = budget
        self.burn = 0
        self.latest = Usage()
        self.in_price = 0
        self.out_price = 0
    
    def run(self):
        with self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=0.9,
            max_tokens=4096,
            stream=True,
            stop=None
        ) as stream:
            for chunk in stream:
                self.log(chunk.choices[0].delta.content)
    
    def get_latest_burn(self):
        return self.in_price * self.latest.input_tokens + self.out_price * self.latest.output_tokens
        
    def get_burn(self): 
        return self.burn

def count_tok(text, model="gpt-4-turbo"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))