# mariana - synthesis at scale

Research agent that browses arxiv to answer your question. \\  

Humanity's best ideas have been interdisciplinary: for example, deep learning was ushered in by researchers with deep expertise in cognitive science and computer science. 
However, minds that can synthesize new insights from multiple subjects are rare. 
Fundamentally, our brains weren't designed for large-scale information synthesis. 
Nobody can hold 100 papers in their working memory at once (we can barely hold seven digits).
But we can engineer AI to do exactly that, and more. 
Project Mariana asks what synthesis at scale using AI might look like.

# how to run

1) create .env file and set your OpenAI, Anthropic, Groq api keys
2) ```python main.py --query "why do primate brains have a hippocampus and why might AI systems want one?"```

# reports

Check out some reports Mariana generated at /reports. The prompting research questions were:
- "AI architectural inspirations to draw from basal ganglia & hippocampus function"
- "how to reward language in LLMs for alphago-like self-play"

# design philosophy
- maximally exploit LLM's working memory (context window) advantage over humans
- quality of research should scale with spend budget
- agent should search to load diverse and high quality info into context 

# observations
- claude3-opus gets argument types wrong ~50% when using tools (functions)
- quality of report with first 3 pages of papers in context >> only abstract of papers in context 

# TODO
- [X] OpenAI & Groq integration
- [ ] logging
- [ ] how to measure quality vs. $ burn? 
- [ ] continued learning: use memory & improve report
- [ ] clean pdf readings 