from dotenv import load_dotenv
from prompt import main_prompt, obs_prompt
from exa_py import Exa
import urllib, urllib.request, json
import os
import shutil
import anthropic
from pypdf import PdfReader

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=os.getenv("ANTHROPIC"),
)
load_dotenv()
exa = Exa(os.getenv("EXA"))
in_cost = 15/1000000 # $0.015/1K
out_cost = 75/1000000 # $0.075/1K

# gpt4 cost
# $0.01/1k 
# $0.03/1k

# save pdfs to memory/raw
# TOOL
def write_report(title, text):
    with open(f'reports/{title}.md', 'w') as f:
        f.write(text)
        exit(-1)

def save_papers(papers):
    res = []
    for paper in papers:
        title,url = paper['title'], paper['url']
        url = url.replace('/abs/', '/pdf/')
        filename = title + ".pdf"
        urllib.request.urlretrieve(url, f"memory/raw/{filename}")
        res.append(f'saving paper {url} to memory/raw/{filename}')
        print(f'saving paper {url} to memory/raw/{filename}')
    return res

# stuff
def return_first_page(files):
    pdf_messages = []
    for file in files:
        reader = PdfReader(file)
        first_5_pages = '\n'.join([page.extract_text() for page in reader.pages[:3]])
        pdf_messages.append({file : first_5_pages})
    return pdf_messages
    
# TOOOL
'''
    {
        "name": "search_arxiv",
        "description": "Search arxiv.org for papers matching a query.",
        "input_schema": {
            "type": "object", 
            "properties": {
                "query": {"type": "string", "description": "Search query string."},
                "max_results": {"type": "integer", "description": "Maximum number of results. Must not exceed 10"}
            },
            "required": ["query", "start", "end", "max_results"]
        }
    },'''
def search_arxiv(query : str, max_results=10):
    query = query.replace(" ", "%20")
    url = f'http://export.arxiv.org/api/query?search_query=all:{query}&sortBy=lastUpdatedDate&sortOrder=descending&max_results={max_results}'
    data = urllib.request.urlopen(url)
    res = data.read().decode('utf-8')
    print(f'search_arxiv result: {res}')
    return res

# returns arxiv links
# TOOL
def search_exa(query, start, end, max_results=10):
    res = exa.search_and_contents(
        query, 
        text={"start_crawl_date":start, "end_crawl_date":end},
        include_domains=["https://arxiv.org"],
        category="papers",
        num_results=max_results
        ).results
    result = {r.title:r.url for r in res}
    print(f'search_exa result: {result}')
    return result

# if persist, move files in memory/working to memory/episodic
# TOOL
def clear_working_memory(persist=True):
    try:
        if persist:
            for file in os.listdir("memory/working"):
                shutil.move(f"memory/working/{file}", f"memory/episodic/{file}")
        else:
            for file in os.listdir("memory/working"):
                os.remove(f"memory/working/{file}")
        print(f'working memory cleared successfully')
        return True
    except Exception as e:
        print(e)
        return False

# read abstract and decide on which papers to load into context
# TOOL
def create_context(papers):
    context = "<documents>\n"
    for i, paper in enumerate(papers, start=1):
        context += f'<document index="{i}">\n'
        context += f'<source>{paper["url"]}</source>\n'
        context += f'<document_content>{paper["abstract"]}</document_content>\n'
        context += '</document>\n'
    context += '</documents>\n'
    print(f'create_context result: {context}')
    return context

def execute_tool(tool_name, tool_input):
    if tool_name == "save_papers":
        return save_papers(tool_input["papers"])
    elif tool_name == "search_arxiv":
        return search_arxiv(tool_input["query"], tool_input["max_results"])
    elif tool_name == "search_exa":
        return search_exa(tool_input["query"], tool_input["start"], tool_input["end"], tool_input["max_results"])
    elif tool_name == "clear_working_memory":
        return clear_working_memory(tool_input["persist"])
    elif tool_name == "create_context":
        return create_context(tool_input["papers"])
    elif tool_name == 'return_first_page':
        return return_first_page(tool_input["files"])
    elif tool_name == 'write_markdown_report':
        return write_report(tool_input["title"], tool_input["markdown_report"])
    else:
        raise ValueError(f"Unknown tool: {tool_name}")

def run_agent(query, budget):
    messages = [{"role": "user", "content": main_prompt(query)}]
    tools = [
    {
        "name": "write_markdown_report",
        "description": "Write your final report that answers the scientists' question",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Title of the report"
                },
                "markdown_report": {
                    "type": "string",
                    "description": "A rigorous, detailed, actionable and beautifully formatted markdown report that answers the scientists' final question. You should cite the title and link of all the papers you read at the bottom."
                }
            },
            "required": ["markdown_report", "title"]
        }
    },
    {
        "name": "return_first_page",
        "description": "Extract the text from the first page of each PDF file in a list.",
        "input_schema": {
            "type": "object",
            "properties": {
                "files": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of file paths to PDF files."
                }
            },
            "required": ["files"]
        }
    },
    {
        "name": "save_papers",
        "description": "Save a list of paper links to memory/raw directory.",
        "input_schema": {
            "type": "object",
            "properties": {
                "papers": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "url": {"type": "string"}
                        },
                        "required": ["title", "url"]
                    },
                    "description": "List of paper links to save."
                }
            },
            "required": ["papers"]
        }
    },

    {
        "name": "search_exa",
        "description": "Search exa.ai for arxiv paper links matching a query.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query string."},
                "start": {"type": "string", "description": "Start date for search, e.g. '2022-01-01'."},
                "end": {"type": "string", "description": "End date for search, e.g. '2023-06-01'."},
                "max_results": {"type": "integer", "description": "Maximum number of results. Must not exceed 10"}
            },
            "required": ["query", "start", "end", "max_results"]
        }
    },
    {
        "name": "clear_working_memory", 
        "description": "Clear files from memory/working directory, optionally moving them to memory/episodic.",
        "input_schema": {
            "type": "object",
            "properties": {
                "persist": {
                    "type": "boolean", 
                    "description": "If true, move files to memory/episodic before clearing. If false, delete them."
                }
            },
            "required": ["persist"]
        }
    },
    {
        "name": "create_context",
        "description": "Create a context string containing paper abstracts.",
        "input_schema": {
            "type": "object",
            "properties": {
                "papers": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "url": {"type": "string"},
                            "abstract": {"type": "string"}
                        },
                        "required": ["url", "abstract"]
                    },
                    "description": "List of papers to include in context."
                }
            },
            "required": ["papers"]
        }
    }
    ]
    obs = []
    spent = 0

    def handle_tool(msgs):
        for msg in msgs:
            print(type(msg))
            if type(msg) == anthropic.types.text_block.TextBlock:  
                print(f'message:')
                print(msg)
                messages.append({"role": "assistant", "content": msg.text})
            elif type(msg) == anthropic.types.beta.tools.tool_use_block.ToolUseBlock:
                print(f'tool use:')
                tool = msg
                print(tool)
                result = execute_tool(tool.name, tool.input)
                obs.append({"tool_name": tool.name, "tool_input": tool.input, "tool_result": result})

    while spent < budget:
        left_out_toks = int((budget-spent)/out_cost)
        message = client.beta.tools.messages.create(
                max_tokens=left_out_toks if left_out_toks < 4096 else 4096,
                messages=messages,
                tools=tools,
                model="claude-3-opus-20240229"
            ) 

        cost = in_cost*message.usage.input_tokens + out_cost*message.usage.output_tokens
        spent += cost
        handle_tool(message.content)
        print(f'in_toks: {message.usage.input_tokens} | out_toks: {message.usage.output_tokens} |  msg cost: ${cost} | total cost: ${spent}')
        
        messages.append({"role": "user", "content": obs_prompt(obs)})
        obs = []
        print("new user prompt:")
        print(messages[-1])

def main():
    query = 'what are the greatest shortcomings of our current AI systems, and how can we take inspiration from the human brain to solve them?'#input()
    budget = 5
    run_agent(query, budget)

main()

# NOTE
# claude opus still makes a lot of mistakes
# it gets type of tools wrong