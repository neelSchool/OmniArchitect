# OmniArchitect  
**Natural language-driven urban infrastructure optimization and 3D visualization for sustainable cities**

## Overview  

**OmniArchitect** is an AI-powered system that transforms natural language descriptions into spatial and structural constraints for **optimal infrastructure placement** within a **grid-like city model**.  

By combining **natural language processing**, **constraint-based optimization**, and **3D browser visualization**, OmniArchitect empowers urban planners, architects, and environmental researchers to **design sustainable cities** that adapt to the challenges of **climate change**, **population growth**, and **limited resources**.  

## Motivation  

As climate change intensifies and resources become scarce, the way we design cities must evolve. Traditional planning is slow, siloed, and often disconnected from data-driven sustainability metrics.  
OmniArchitect aims to bridge that gap by:  
- Allowing **planners to communicate in plain language**, not complex CAD scripts.  
- Embedding **ecological and social constraints** directly into the planning process.  
- Offering **real-time 3D insights** to visualize trade-offs and outcomes.  

## Core Features  

### Natural Language Parsing  
- Converts human-readable requests (e.g. *“Place solar panels on all south-facing roofs near schools”*) into formal spatial and environmental constraints.  
- Leverages LLMs and a domain-specific grammar for city planning semantics.  

### Constraint Optimization  
- Uses multi-objective solvers to balance sustainability, accessibility, and resource efficiency.  
- Supports constraints for:  
  - Energy efficiency  
  - Water and waste systems  
  - Mobility networks  
  - Zoning and density  
  - Green spaces  

### 3D Browser Visualization  
- Generates an **interactive 3D city grid** using **plotly**.  
- Visualizes optimized infrastructure placement and scenario comparisons.  
- Includes layers for solar exposure, emissions, walkability, and more.  

## Tech Stack  

| Layer | Technology |
|-------|-------------|
| **Language Understanding** | Transformers / Regex fallback|
| **Constraint Solver** | OR-Tools / custom multi-objective optimizer |
| **Backend** | Python |
| **3D Visualization** | Plotly |
| **Data Layer** | Urban Block Dataset (NYC, LA, London) |

## Example Usage  

```bash
# Clone and run
git clone https://github.com/yourusername/OmniArchitect.git
cd OmniArchitect
pip install -r requirements.txt
python3 main.py
firefox city_plan_3d.html
```

## Future Work
- Further train the domain specific transformer model (base flat-T5) with more data with HuggingFace to improve heuristics.
- Add 3D assets to plotly visualiser for a more intuitive viewing experience.

## How you can Help
- Architecture Firms: Please use the system and send feedback to improve the experience for other
- Environmental Researcher: Share any datasets that would be more appropriate to your research and I can help with training and ML side of it.
- Corporations: If you have any Computing or GPU credits or unused hardware that I could use please contact me.
- Individuals: Talk to local builders and see if they can benefit from such software and just spread the word to make Architecture more sustainable.

## Contact Info
Feel free to contact me at **neel.mehendale@gmail.com** at any time whether it is about sponsorships, contributing or production usage.
I will try my best to respond within 7 days to any requests with any information requested or request an online meeting to discuss your request further.

- System, Explanations and Work by Neel Mehendale (as part of my Sustainability Initiative).
