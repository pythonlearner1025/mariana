# mariana - deep search agent

Search agent that does deep saerch to answer your question.    

The core idea is that the quality of search should scale with the value of the answer to the query (quantified by $ spend budget)  

I'm betting that for queries like: 
- candidate compounds for new drug synthesis (drug development)
- what can we learn from field A to apply to field B (research)
- everyone who's working on X currently (recruiting)

current search engines are bad at answering them, and the value of answering queries justifies long wait times & search cost.  

*Experimental*, only supports arxiv search using Exa & arxiv API currently for research related queries.

# how to run
1) create .env file and set your OpenAI, Anthropic, Groq api keys
2) ```python main.py --query "why do primate brains have a hippocampus and why might AI systems want one?" --budget 5 --agent openai```

# reports
Check out some reports Mariana generated at /reports. The queries were:
- "AI architectural inspirations to draw from basal ganglia & hippocampus function"
- "how to reward language in LLMs for alphago-like self-play"

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