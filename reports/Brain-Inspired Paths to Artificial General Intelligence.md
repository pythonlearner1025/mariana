# Brain-Inspired Paths to Artificial General Intelligence

## Abstract
Despite remarkable progress, current artificial intelligence (AI) systems based on deep learning neural networks still fall short of human-like intelligence in crucial ways. They struggle with abstraction, causal reasoning, generalizing to novel situations, building coherent world models, and learning efficiently from small amounts of data. Solving these challenges to create artificial general intelligence (AGI) will require moving beyond approaches focused solely on scaling up pattern recognition in disembodied neural networks. The most promising path forward is to take inspiration from the only known example of general intelligence - the animal brain - and design AI systems that incorporate its key computational and architectural principles. Three fruitful directions are: 1) combining neural networks with symbolic reasoning in synergistic neuro-symbolic architectures, 2) training embodied agents with intrinsic curiosity to acquire general skills through open-ended interaction with complex environments, and 3) leveraging flexible temporal hierarchies and transient neural dynamics for cognitive flexibility. By grounding AI more firmly in computational neuroscience and centering real-world interaction and temporal structure, we can accelerate progress towards robustly capable and adaptive AGI.

## Limitations of Current AI
Today's AI excels at narrow perception and pattern recognition tasks, fueled by training large neural networks on massive labeled datasets. However, as many recent analyses have noted, they continue to struggle with core capabilities of human intelligence [1-3]:
- Abstraction: forming high-level concepts and systematic rules 
- Causal reasoning: modeling causal relationships and drawing inferences
- Out-of-distribution generalization: robust performance in novel situations
- World models: coalescing knowledge into coherent representations of the environment and agents 
- Sample efficiency: rapid learning from small numbers of examples
- Energy efficiency: matching human computational abilities with vastly less power consumption

These deficiencies stem from several properties of standard deep learning approaches:
1. Learning solely from static datasets without interaction or feedback
2. Monolithic architectures that do not decompose knowledge 
3. Emphasis on input-output mappings vs. modeling data-generating processes
4. Opaque representations that are not interpreted symbolically
5. Feedforward processing that ignores temporal structure

While scaling up models and training data has yielded performance gains, extrapolating this strategy is unlikely to bridge the gap to human-level AGI [1,2]. Matching the generality and flexibility of human intelligence will require qualitatively different computational principles.  

## Brain-Inspired Paradigms for AGI
The animal brain provides the best template for general intelligence that we have [4,5]. Three key brain-inspired paradigms stand out as promising directions for overcoming the limitations of current AI:

### Neuro-Symbolic Architectures  
Biological brains seamlessly integrate two distinct yet synergistic modes of information processing [6,7]:
1. Sub-symbolic: neural networks for pattern recognition, generalization, and learning
2. Symbolic: discrete compositional representations for abstraction, reasoning, and recursion

Current neuro-symbolic AI architectures aim to replicate this duality by building hybrid systems that combine neural networks with symbolic programs [6,7]. The networks handle perception and provide statistical learning, while the symbolic components perform reasoning and leverage abstract knowledge. Importantly, the full potential of neuro-symbolic AI lies in tight integration and interaction between these levels, rather than just using them as separate modules [7]. Some key challenges are how to learn symbolic representations from data, leverage them to guide the networks, and use network outputs to improve the symbolic knowledge. Early successes in areas like visual question answering [8] and language-guided robotics [9] highlight the promise of this approach. Creating a virtuous cycle between neural learning and symbolic reasoning, like in the brain, is crucial for achieving flexible intelligence.

### Curiosity-Driven Embodied Interaction
Human intelligence emerges through an extended period of playing, practicing, and exploring in a complex physical and social environment [5,10]. In contrast, most current AI is trained on large but static datasets of disembodied data, limiting its ability to reason about the causal structure of the world and generalize to new contexts. Recently, the paradigm of embodied AI, where agents learn through interaction with simulated or real environments, has seen a resurgence [11,12]. Of particular relevance are intrinsically-motivated approaches driven by curiosity and multi-task learning [13,14]. In this framework, the agent seeks to maximize its knowledge and skills by setting its own goals and subgoals, rather than optimizing a narrow, externally-specified reward function. This leads to the self-supervised acquisition of reusable models and abilities. Learning progress itself becomes rewarding, creating a positive feedback loop.

Compared to a standard deep reinforcement learning setup, this kind of curiosity-driven, open-ended learning has important advantages: 1) produces an emergent curriculum where the agent is always at the edge of its competence, 2) enables learning many interrelated skills simultaneously, and 3) grounds knowledge in sensorimotor experience to support reasoning and generalization [13,14]. Developing sophisticated world models and the meta-cognitive ability to reflect on and leverage them flexibly is a key milestone on the path to AGI. Computational accounts of human cognitive development in terms of intrinsically-motivated learning in embodied agents [10,15] provide a roadmap that could be realized in artificial systems.

### Flexible Temporal Hierarchies
Brains are highly dynamical systems that rapidly construct and dissolve patterns of neural activity on multiple timescales [16-18]. In particular, the precise synchronization of neuronal firing across brain areas has been proposed as a mechanism for dynamically binding together information into coherent thoughts and mental states [16]. Rather than time-invariant attractors, cognition unfolds through transient dynamics and a progression of metastable states [17]. Top-down and bottom-up influences are integrated through nested oscillations at different frequencies, e.g. gamma activity within slower theta rhythms [16,18]. These temporal hierarchies reflect the hierarchical organization of cognitive representations and allow for rapid reconfiguration of functional networks on the fly.

In contrast, most deep learning systems rely on feedforward architectures and static training, lacking the rich temporal structure of brain activity [19]. Incorporating more flexible and neurally-plausible temporal dynamics into AI systems could yield several benefits. Synchrony-based binding can support the dynamic construction of compositional representations [20,21]. Transient trajectories through state space allow for fluid sequences of thoughts and behaviors [22]. Nested oscillations naturally segment information into chunks while maintaining temporal order. While some recurrent neural network approaches exploit multiscale temporal structure [23], brain-inspired dynamical primitives such as oscillations, traveling waves [24], and metastable attractors [25] remain under-explored in AI. A tighter integration of computational neuroscience models of temporal hierarchies with deep learning could significantly boost the cognitive flexibility of artificial neural networks. 

## Conclusions
We have argued that overcoming key limitations of current AI to achieve human-like AGI will require moving beyond approaches that simply scale up pattern recognition in disembodied neural networks. A more promising path is to design AI systems based on computational principles of biological brains, which provide the sole existing proof-of-concept for general intelligence. 

We highlighted three especially relevant brain-inspired paradigms: 1) neuro-symbolic architectures that synergistically combine neural networks and symbolic programs, 2) curiosity-driven learning through embodied interaction with complex environments to acquire general world models and skills, and 3) flexible temporal hierarchies and transient neural dynamics that support fluid cognitive processes. Each of these areas has seen promising initial developments in AI, but major open challenges remain.

In particular, finding synergistic combinations of neural and symbolic representations, designing objective functions and environments for open-ended learning, and leveraging neurally-plausible temporal dynamics are key priorities. Making progress will require AI researchers to engage deeply with computational neuroscience and center real-world interaction and temporal structure as organizing principles. Likewise, neuroscientists can benefit from using the conceptual frameworks and modeling tools of AI as a common language.

Achieving these ambitious goals will take a concerted effort from the research community. But if the last decade of AI has taught us anything, it's that surprising breakthroughs are possible when we unite around a common mission. With the right interdisciplinary collaborations and brain-inspired approaches, we believe artificial general intelligence that matches the miracle of the human mind is within reach. The time is now to make it happen.

## References
[1] Lake, B. M., Ullman, T. D., Tenenbaum, J. B., & Gershman, S. J. (2017). Building machines that learn and think like people. Behavioral and Brain Sciences, 40.
[2] Marcus, G. (2018). Deep learning: A critical appraisal. arXiv preprint arXiv:1801.00631.
[3] Bengio, Y. (2019). From System 1 Deep Learning to System 2 Deep Learning. NeurIPS 2019.
[4] Hassabis, D., Kumaran, D., Summerfield, C., & Botvinick, M. (2017). Neuroscience-inspired artificial intelligence. Neuron, 95(2), 245-258.
[5] Richards, B. A., et al. (2019). A deep learning framework for neuroscience. Nature neuroscience, 22(11), 1761-1770.
[6] d'Avila Garcez, A., Lamb, L. C., & Gabbay, D. M. (2008). Neural-symbolic cognitive reasoning. Springer Science & Business Media.
[7] Besold, T. R., et al. (2017). Neural-symbolic learning and reasoning: A survey and interpretation. arXiv preprint arXiv:1711.03902.
[8] Yi, K., et al. (2018). Neural-symbolic VQA: Disentangling reasoning from vision and language understanding. arXiv preprint arXiv:1810.02338.
[9] Arkin, J., et al. (2020). Multimodal Hierarchical Reinforcement Learning Policy for Task-Oriented Visual Dialog. arXiv preprint arXiv:2002.01554.
[10] Oudeyer, P. Y., Kaplan, F., & Hafner, V. V. (2007). Intrinsic motivation systems for autonomous mental development. IEEE transactions on evolutionary computation, 11(2), 265-286.
[11] Pfeifer, R., Bongard, J., & Grand, S. (2007). How the body shapes the way we think: a new view of intelligence. MIT press.
[12] Savva, M., et al. (2019). Habitat: A Platform for Embodied AI Research. arXiv preprint arXiv:1904.01201.
[13] Pathak, D., Agrawal, P., Efros, A. A., & Darrell, T. (2017). Curiosity-driven exploration by self-supervised prediction. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition Workshops (pp. 16-17).
[14] Eysenbach, B., Gupta, A., Ibarz, J., & Levine, S. (2018). Diversity is all you need: Learning skills without a reward function. arXiv preprint arXiv:1802.06070.
[15] Gopnik, A. Meltzoff, A.N., Kuhl, P.K., (1999). The scientist in the crib: Minds, brains, and how children learn. William Morrow & Co.
[16] Engel, A. K., Fries, P., & Singer, W. (2001). Dynamic predictions: oscillations and synchrony in top–down processing. Nature Reviews Neuroscience, 2(10), 704-716.
[17] Tognoli, E., & Kelso, J. S. (2014). The metastable brain. Neuron, 81(1), 35-48.
[18] Canolty, R. T., & Knight, R. T. (2010). The functional role of cross-frequency coupling. Trends in cognitive sciences, 14(11), 506-515.
[19] Yamins, D. L., & DiCarlo, J. J. (2016). Using goal-driven deep learning models to understand sensory cortex. Nature neuroscience, 19(3), 356.
[20] Hummel, J. E., & Holyoak, K. J. (1997). Distributed representations of structure: A theory of analogical access and mapping. Psychological review, 104(3), 427.
[21] van der Velde, F., & de Kamps, M. (2006). Neural blackboard architectures of combinatorial structures in cognition. Behavioral and Brain Sciences, 29(1), 37-70.
[22] Rabinovich, M., Huerta, R., & Laurent, G. (2008). Neuroscience. Transient dynamics for neural processing. Science, 321(5885), 48-50.
[23] Chung, J., Ahn, S., & Bengio, Y. (2016). Hierarchical multiscale recurrent neural networks. arXiv preprint arXiv:1609.01704.
[24] Muller, L., Chavane, F., Reynolds, J., & Sejnowski, T. J. (2018). Cortical travelling waves: mechanisms and computational principles. Nature Reviews Neuroscience, 19(5), 255-268.
[25] Deco, G., & Jirsa, V. K. (2012). Ongoing cortical activity at rest: criticality, multistability, and ghost attractors. Journal of Neuroscience, 32(10), 3366-3375.