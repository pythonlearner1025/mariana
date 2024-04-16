# mariana - synthesis at scale
Humanity's best ideas have been interdisciplinary: for example, deep learning was ushered in by researchers with deep expertise in cognitive science and computer science. 
However, minds that can synthesize new insights from multiple subjects are rare. 
Fundamentally, our brains weren't designed to perform such sweeping synthesis. 
Nobody can hold 100 papers in their working memory at once (we can barely hold seven digits).
But we can engineer AI to do exactly that, and more. 
Project Mariana asks what massive synthesis using AI might look like.

# design philosophy
- maximally exploit the working memory (context window) advantage LLMs have over humans 
- quality of research should scale with spend budget
- agent should search to load diverse and high quality info into context 

# observations
- claude3-opus gets argument types wrong ~50% when using tools (functions)
- quality of report with first 3 pages of papers in context >> only abstract of papers in context 

# TODO
- [ ] how to measure quality vs. $ burn? 
- [ ] continued learning: use memory & improve report
- [ ] clean pdf readings 
- [ ] gpt4 & Mixtral integration