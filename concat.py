import os
import re
import tiktoken

#target_dir = '/Users/minjunes/tinygrad'
target_dir = '/Users/minjunes/Downloads/rabbit home'
prompt = '''Analyze this repository to give me an overall idea of how the codebase works. Write a clear README.md file
that explains the purpose of the repository, the core components of it, and how it can be run.'''


blacklist_folder = [
    r'^\.',  # Blacklist files and directories starting with a dot
    r'\.pyc$',  # Blacklist .pyc files
    r'\.git',  # Blacklist .git directory
    r'\.idea',  # Blacklist .idea directory
    r'\.vscode',  # Blacklist .vscode directory
    r'\.DS_Store',  # Blacklist .DS_Store files
    r'\.png$',
    r'^\.datasets',
    r'node_modules',
    r'styles',
    r'images',
    r'bin',
    r'typescript'
]  # Blacklist PNG files

blacklist_ext = [
    '.png', '.jpg', '.ico', '.oga', '.mp3', '.ttf', '.woss', '.pdf', '.h', '.wav', '.pyc', '.pth', '.gz', '.jpeg', '.swp', '.mlmodel', '.hwx', '.weights',
    '.pack', '.idx', '.sample', '.md', '.yml', '.html', '.mm', '.c', '.xml', '.js', '.0', '.toml', '.old', '.golden', '.m', '.swift', '.cpp', '.csv', '.s', '.cc', '.ini',
    '.wandb', '.yaml', '.plist', '.sh' ,'.log', '.json', '.txt'
]

whitelist_ext = ['.ts', '.py', '.sh']

def is_blacklisted(name):
  #print(os.path.splitext(name))
  for pattern in blacklist_folder:
    if re.match(pattern, name, re.IGNORECASE):
      return True
  if os.path.splitext(name)[1].lower() not in whitelist_ext:
    return True
  print(name)
  print(os.path.isdir(name))
  if not os.path.isdir(name) and os.path.splitext(name)[1] == '':
    return True
  return False

def count_tok(text, model="gpt-4-turbo", allowed_special={'<|endoftext|>'}):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text, allowed_special=allowed_special))

def recurse(prompt, folder, exts={}):
  for f in os.listdir(folder):
    f = os.path.join(folder, f)
    if is_blacklisted(f):
      continue
    _,ext = os.path.splitext(f)
    if os.path.isdir(f):
      print(f)
      prompt += recurse('',f, exts=exts)
      continue
    exts[ext] = exts.get(ext, 0) + 1
    try:
      with open(f, 'r') as file:
        text = file.read()
    except Exception as e:
      continue
    prompt += '<document>\n'
    prompt += f'path: {f}'
    prompt += text + '\n'
    prompt += '</document>\n'
  return prompt
exts = {}
prompt = recurse(prompt, target_dir, exts=exts)
exts = sorted([(k,v) for k,v in exts.items()], key=lambda x:x[1])[::-1]
print(exts)
toks = count_tok(prompt)
print(f'{toks} tokens')