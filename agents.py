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

class OAIAgent:
    def __init__(self, key, instruction, budget, model='gpt-4-turbo-2024-04-09'):
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
        self.instruction = instruction
        self.assistant = self.client.beta.assistants.create(
                instructions=instruction,
                model=self.model,
                tools=self.tools
            )
        self.thread = None
    
    def call(self, msg):
        if not self.thread:
            self.thread = self.client.beta.threads.create(
                messages = [{'role': 'user','content': msg}]
            )
        else:
            self.thread = self.client.beta.threads.create(
                messages = self.messages
            )
        input_tokens = count_tok(msg)
        output_tokens = 0
        self.messages.append({'role': 'user', 'content': msg})
        with self.client.beta.threads.runs.stream(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            ) as stream:
            for event in stream:
                if isinstance(event, openai.types.beta.assistant_stream_event.ThreadRunStepDelta):
                    txt = event.data.delta.step_details.tool_calls[0].function.arguments
                    output_tokens += count_tok(txt)
                    print(txt, end='', flush=True)
                elif isinstance(event, openai.types.beta.assistant_stream_event.ThreadMessageDelta):
                    txt = event.data.delta.content[0].text.value
                    output_tokens += count_tok(txt)
                    print(txt, end='', flush=True)
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
                        print('== calling function ==')
                        print(function, args)
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
                    print(event.data.delta.step_details.tool_calls[0].function.arguments, end='', flush=True)
                elif isinstance(event, openai.types.beta.assistant_stream_event.ThreadMessageDelta):
                    txt = event.data.delta.content[0].text.value
                    output_tokens += count_tok(txt)
                    print(event.data.delta.content[0].text.value, end='', flush=True)
                elif isinstance(event, openai.types.beta.assistant_stream_event.ThreadRunRequiresAction):
                    print(event)
                    req = event.data.required_action
                    tool_calls = req.submit_tool_outputs.tool_calls
                    outs = []
                    for tool in tool_calls:
                        call_id = tool.id
                        function = tool.function.name
                        output_tokens += count_tok(tool.function.arguments)
                        output_tokens += count_tok(tool.function.name)
                        args = json.loads(tool.function.arguments)
                        print('== calling function ==')
                        print(function, args)
                        output = execute_tool(function, args)
                        outs.append({'tool_call_id': call_id, 'output': f'{output}'})  
                    self.submit_to_run(event, outs)

        self.latest.input_tokens = input_tokens
        self.latest.output_tokens = output_tokens
        self.burn += self.get_latest_burn()
    
    def get_latest_burn(self):
        return self.in_price*self.latest.input_tokens + self.out_price*self.latest.output_tokens
        
    def get_burn(self): 
       return self.burn

class AnthropicAgent:
    def __init__(self, key, budget, model='claude-3-opus-20240229'):
        self.client = Anthropic(api_key=key)
        self.tools = json.loads(open('tools/anthropic_tools.json').read())
        self.budget = budget
        self.burn = 0
        self.in_price = 15/1000000
        self.out_price = 75/1000000
        self.messages = []
        self.model = model
        self.latest = Usage()
    
    def call(self, msg : str):
        self.messages.append({'role': 'user', 'content': msg})
        message = self.client.beta.tools.messages.create(
            max_tokens=4096,
            messages=self.messages,
            tools=self.tools,
            model=self.model
        ) 

        cost = self.in_price*message.usage.input_tokens + self.out_price*message.usage.output_tokens
        self.burn += cost
        obs = self.handle_tool(message.content)
        self.messages.append({"role": "user", "content": obs_prompt(obs)})
        return message
    
    def handle_tool(self, msgs):
        obs = []
        for msg in msgs:
            if type(msg) == anthropic.types.text_block.TextBlock:  
                self.messages.append({"role": "assistant", "content": msg.text})
            elif type(msg) == anthropic.types.beta.tools.tool_use_block.ToolUseBlock:
                tool = msg
                result = execute_tool(tool.name, tool.input)
                obs.append({"tool_name": tool.name, "tool_input": tool.input, "tool_result": result})
        return obs

    def get_latest_burn(self):
        return self.in_price*self.latest.input_tokens + self.out_price*self.latest.output_tokens
        
    def get_burn(self): 
       return self.burn

class GroqAgent:
    # currently unable to function call, so technically not an agent
    # but would be interesting to see what it can do
    def __init__(self, key, sys_prompt, budget, model='mixtral-8x7b-32768'):
        self.client = Groq(api_key=key)
        self.model = model
        self.messages = [{
            'role': 'user',
            'content': sys_prompt
        }]
        self.budget = budget
        self.burn = 0
        self.latest = Usage()
    
    def call(self, msg):
        self.messages.append({
            'role': 'user',
            'content': msg
        })
        with self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=0.9,
            max_tokens=4096,
            stream=True,
            stop=None
        ) as stream:
            for chunk in stream:
                print(chunk.choices[0].delta.content, end="")
    
    def get_latest_burn(self):
        return self.in_price*self.latest.input_tokens + self.out_price*self.latest.output_tokens
        
    def get_burn(self): 
       return self.burn


def count_tok(text, model="gpt-4-turbo"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))