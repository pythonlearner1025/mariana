import urllib, shutil, os
from dotenv import load_dotenv
from pypdf import PdfReader
from exa_py import Exa

load_dotenv()
exa = Exa(os.getenv("EXA"))

def execute_tool(tool_name, tool_input):
    if tool_name == "save_papers":
        return save_papers(tool_input["papers"])
    elif tool_name == "search_arxiv":
        return search_arxiv(tool_input["query"], max_results=tool_input["max_results"])
    elif tool_name == "search_exa":
        return search_exa(tool_input["query"], tool_input["start"], tool_input["end"], max_results=tool_input["max_results"])
    elif tool_name == "clear_working_memory":
        return clear_working_memory(tool_input["persist"])
    elif tool_name == "create_context":
        return create_context(tool_input["papers"])
    elif tool_name == 'return_first_n_pages':
        return return_first_n_pages(tool_input["files"])
    elif tool_name == 'write_markdown_report':
        return write_markdown_report(tool_input["title"], tool_input["markdown_report"])
    else:
        raise ValueError(f"Unknown tool: {tool_name}")

def write_markdown_report(title: str, text: str) -> None:
    '''
    Writes a report with the given title and text content.

    param str title: The title of the report.
    param str text: The text content of the report.
    return None
    '''
    with open(f'reports/{title}.md', 'w') as f:
        f.write(text)
    exit(-1)

def save_papers(papers: list[dict[str, str]]) -> list[str]:
    '''
    Downloads papers from the provided URLs and saves them as PDF files.

    param list[dict[str, str]] papers: A list of dictionaries containing 'title' and 'url' keys.
    return list[str]: A list of strings indicating the saved paper URLs and filenames.
    '''
    res = []
    for paper in papers:
        title, url = paper['title'], paper['url']
        url = url.replace('/abs/', '/pdf/')
        filename = title + ".pdf"
        urllib.request.urlretrieve(url, f"memory/raw/{filename}")
        res.append(f'saving paper {url} to memory/raw/{filename}')
        print(f'saving paper {url} to memory/raw/{filename}')
    return res

def return_first_n_pages(files: list[str], n: int = 3) -> list[dict[str, str]]:
    '''
    Opens PDF files and returns the text from the first n pages of each file.

    param list[str] files: A list of file paths to PDF files.
    param int n: The number of pages to extract text from (default is 3).
    return list[dict[str, str]]: A list of dictionaries where each dictionary contains the file path as the key and the extracted text as the value.
    '''
    pdf_messages = []
    for file in files:
        reader = PdfReader(file)
        first_5_pages = '\n'.join([page.extract_text() for page in reader.pages[:n]])
        pdf_messages.append({file: first_5_pages})
    return pdf_messages

def search_arxiv(query: str, max_results: int = 10) -> str:
    '''
    Performs a search on the arXiv API using the provided query.

    param str query: The search query string.
    param int max_results: The maximum number of results to retrieve (default is 10).
    return str: The search results as a string in XML format.
    '''
    query = query.replace(" ", "%20")
    url = f'http://export.arxiv.org/api/query?search_query=all:{query}&sortBy=lastUpdatedDate&sortOrder=descending&max_results={max_results}'
    data = urllib.request.urlopen(url)
    res = data.read().decode('utf-8')
    print(f'search_arxiv result: {res}')
    return res

def search_exa(query: str, start: str, end: str, max_results: int = 10) -> dict[str, str]:
    '''
    Searches for papers on arXiv using the Exa API.

    param str query: The search query string.
    param str start: The start date for the search in the format 'YYYY-MM-DD'.
    param str end: The end date for the search in the format 'YYYY-MM-DD'.
    param int max_results: The maximum number of results to retrieve (default is 10).
    return dict[str, str]: A dictionary where the keys are the paper titles and the values are the corresponding URLs.
    '''
    res = exa.search_and_contents(
        query,
        text={"start_crawl_date": start, "end_crawl_date": end},
        include_domains=["https://arxiv.org"],
        category="papers",
        num_results=max_results
    ).results
    result = {r.title: r.url for r in res}
    print(f'search_exa result: {result}')
    return result

def clear_working_memory(persist: bool = True) -> bool:
    '''
    Clears the files in the memory/working directory. If persist is True, moves the files to memory/episodic instead.

    param bool persist: Determines whether to move the files to memory/episodic or delete them (default is True).
    return bool: True if the operation is successful, False otherwise.
    '''
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

def create_context(papers: list[dict[str, str]]) -> str:
    '''
    Creates a context string containing paper abstracts.

    param list[dict[str, str]] papers: A list of dictionaries containing 'url' and 'abstract' keys.
    return str: The context string with paper abstracts formatted as XML.
    '''
    context = "<documents>\n"
    for i, paper in enumerate(papers, start=1):
        context += f'<document index="{i}">\n'
        context += f'<source>{paper["url"]}</source>\n'
        context += f'<document_content>{paper["abstract"]}</document_content>\n'
        context += '</document>\n'
    context += '</documents>\n'
    print(f'create_context result: {context}')
    return context
