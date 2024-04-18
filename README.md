# mariana - deep search agent

Search agent that does deep search to answer your question.    

The core idea is that quality of search should scale with the value of answering a query (quantified by $ spend budget)  

I'm betting that for queries like: 
- which chemical compounds might have similar effects as ketamine? (drug discovery)
- How does the basal ganglia work and what can AI researchers learn from it? (AI research)
- Who's built zero-knowledge proof projects? (recruiting)

current search engines are bad at answering them, and the value of answering queries justifies long wait times & search cost.  

*Experimental*, only supports arxiv search using Exa & arxiv API currently for research related queries. 

# how to run
1) create .env file and set your OpenAI, Anthropic, Groq api keys
2) ```python main.py --query "why do primate brains have a hippocampus and why might AI systems want one?" --budget 5 --agent openai```

# example reports
Check out some example reports Mariana generated in /reports. The query was:  
```Why do primate brains have a hippocampus and why might AI systems want one```

# observations
- ```claude-3-opus``` writes best reports, followed by ```gpt-4-turbo-2024-04-09```
- quality of report with first 3 pages of papers in context >> only abstract of papers in context 

# TODO
- [X] OpenAI & Groq integration
- [X] logging
- [ ] more useful than one-shot generation / existing survey papers? 
- [ ] how to measure quality vs. $ burn? 
- [ ] continued learning: use memory & improve report
- [ ] clean pdf readings 