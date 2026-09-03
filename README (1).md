# 🚀 ResearchForge AI

> **A Multi-Agent AI Research & Project Discovery Platform powered by
> LangGraph, LangChain, RAG, Web Search, Academic Research, and Mistral
> AI.**

ResearchForge AI is an intelligent research assistant that transforms a
research question or project idea into a structured, evidence-oriented
research report.

Instead of asking a single LLM to answer a question, ResearchForge AI
uses multiple specialized AI agents. Each agent has a specific
responsibility such as planning, web research, academic research,
document retrieval, analysis, feasibility evaluation, and critical
review.

------------------------------------------------------------------------

## 📌 Table of Contents

-   [What is ResearchForge AI?](#-what-is-researchforge-ai)
-   [Problem Statement](#-problem-statement)
-   [Key Features](#-key-features)
-   [How ResearchForge AI Works](#-how-researchforge-ai-works)
-   [Multi-Agent Architecture](#-multi-agent-architecture)
-   [Agents](#-agents)
-   [Input](#-input)
-   [Output](#-output)
-   [Example Demo](#-example-demo)
-   [Technology Stack](#-technology-stack)
-   [Project Structure](#-project-structure)
-   [Prerequisites](#-prerequisites)
-   [Environment Variables](#-environment-variables)
-   [Backend Setup](#-backend-setup)
-   [Frontend Setup](#-frontend-setup)
-   [Running the Complete Project](#-running-the-complete-project)
-   [API](#-api)
-   [RAG Pipeline](#-rag-pipeline)
-   [LangGraph Workflow](#-langgraph-workflow)
-   [Revision Loop](#-revision-loop)
-   [Mock LLM Mode](#-mock-llm-mode)
-   [Demo Scenarios](#-demo-scenarios)
-   [Troubleshooting](#-troubleshooting)
-   [Security](#-security)
-   [Future Improvements](#-future-improvements)
-   [Interview / Viva Explanation](#-interview--viva-explanation)
-   [License](#-license)

------------------------------------------------------------------------

# 🧠 What is ResearchForge AI?

ResearchForge AI is a **multi-agent AI research platform**.

A user enters a question such as:

``` text
How can AI improve the education system in India?
```

ResearchForge AI then coordinates a group of specialized agents:

``` text
User Question
     ↓
Supervisor
     ↓
Planner
     ↓
 ┌──────────────┬──────────────────┬─────────────┐
 ↓              ↓                  ↓
Web Research   Academic Research   RAG Research
 └──────────────┬──────────────────┴─────────────┘
                ↓
          Research Merge
                ↓
             Analyst
                ↓
          Feasibility
                ↓
              Critic
                ↓
        Revision if required
                ↓
          Final Research
```

The goal is to produce a useful research report rather than a simple
chatbot response.

------------------------------------------------------------------------

# 🎯 Problem Statement

Traditional research often requires a user to manually:

1.  Search the web.
2.  Search academic papers.
3.  Read documents and PDFs.
4.  Collect useful information.
5.  Compare different technologies.
6.  Find datasets.
7.  Analyze possible solutions.
8.  Check technical feasibility.
9.  Identify research gaps.
10. Write a final report.

This process can be slow and difficult.

ResearchForge AI attempts to automate and organize this workflow using a
**LangGraph-based multi-agent system**.

------------------------------------------------------------------------

# ✨ Key Features

## 1. Multi-Agent Research

Multiple specialized agents collaborate on the same research problem.

Instead of one general-purpose LLM doing everything, each agent has a
defined role.

------------------------------------------------------------------------

## 2. Supervisor Agent

The Supervisor understands the user's research request and coordinates
the research workflow.

Responsibilities:

-   Understand the research problem.
-   Determine what kind of research is required.
-   Coordinate downstream agents.
-   Maintain the overall research objective.

------------------------------------------------------------------------

## 3. Research Planner

The Planner converts the user's question into a structured research
plan.

Example:

``` text
Research Question:
How can AI improve education in India?

Plan:

1. Identify major education challenges.
2. Find existing AI applications.
3. Search academic research.
4. Identify technologies.
5. Find datasets.
6. Compare approaches.
7. Analyze implementation challenges.
8. Identify research gaps.
9. Evaluate feasibility.
```

------------------------------------------------------------------------

## 4. Web Research Agent

The Web Research Agent searches online sources using web search
infrastructure such as Tavily.

It can collect information about:

-   Existing solutions.
-   Current technologies.
-   Industry applications.
-   Recent developments.
-   Practical implementation approaches.

------------------------------------------------------------------------

## 5. Academic Research Agent

The Academic Research Agent focuses on academic and research
information.

It can be used to discover:

-   Research papers.
-   Academic studies.
-   Research topics.
-   Existing methodologies.
-   Scientific approaches.

Academic search providers can be changed independently as the project
evolves.

------------------------------------------------------------------------

## 6. RAG Research Agent

The RAG Research Agent allows ResearchForge AI to use user-provided
documents.

Typical flow:

``` text
PDF / Document
      ↓
Document Loader
      ↓
Text Splitting
      ↓
Embeddings
      ↓
Chroma Vector Database
      ↓
Retriever
      ↓
Relevant Document Chunks
      ↓
RAG Agent
```

This makes it possible to combine external research with information
from the user's own documents.

------------------------------------------------------------------------

## 7. Research Merge

The Research Merge stage combines findings from:

``` text
Web Research
      +
Academic Research
      +
RAG Research
```

The combined research is passed to the Analyst.

------------------------------------------------------------------------

## 8. Analyst Agent

The Analyst synthesizes the collected information.

The analysis is structured around:

1.  Problem understanding.
2.  Existing solutions.
3.  Research findings.
4.  Technical approaches.
5.  Dataset availability.
6.  Technology comparison.
7.  Recommended approach.
8.  Major challenges.
9.  Research gaps.
10. Project opportunities.

The Analyst is instructed not to intentionally invent information and to
distinguish evidence from assumptions.

------------------------------------------------------------------------

## 9. Feasibility Agent

The Feasibility Agent evaluates whether a proposed project or solution
is practically buildable.

It can consider:

-   Technical feasibility.
-   Dataset availability.
-   Technology requirements.
-   Implementation complexity.
-   Infrastructure requirements.
-   Major risks.
-   Practical challenges.

------------------------------------------------------------------------

## 10. Critic Agent

The Critic reviews the generated analysis.

It looks for:

-   Missing information.
-   Unsupported claims.
-   Weak reasoning.
-   Contradictions.
-   Unrealistic recommendations.
-   Missing challenges.
-   Areas requiring additional analysis.

The Critic can return a revision verdict.

Example:

``` text
VERDICT: REVISE

The analysis requires additional discussion
of data privacy and regional language support.
```

------------------------------------------------------------------------

## 11. Conditional Revision Loop

One of the important LangGraph features is the revision loop.

Conceptually:

``` text
Analyst
   ↓
Feasibility
   ↓
Critic
   ↓
 ┌───────────────┐
 │               │
PASS           REVISE
 │               │
 ↓               ↓
Final          Analyst
                 ↓
             Feasibility
                 ↓
               Critic
```

The workflow can revise the analysis when the Critic identifies
important issues.

A revision limit is used to prevent an infinite loop.

------------------------------------------------------------------------

## 12. Mistral LLM

ResearchForge AI uses Mistral through LangChain for LLM-based reasoning.

The configured model can be changed from the central LLM configuration.

Example:

``` python
ChatMistralAI(
    model="mistral-small-2506",
    temperature=0,
    api_key=os.getenv("MISTRAL_API_KEY")
)
```

------------------------------------------------------------------------

# 🔄 How ResearchForge AI Works

The complete conceptual pipeline is:

``` text
                    USER
                     │
                     ▼
             Research Question
                     │
                     ▼
              ┌─────────────┐
              │ Supervisor  │
              └──────┬──────┘
                     ▼
              ┌─────────────┐
              │   Planner   │
              └──────┬──────┘
                     │
       ┌─────────────┼─────────────┐
       ▼             ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Web         │ │ Academic    │ │ RAG         │
│ Researcher  │ │ Researcher  │ │ Researcher  │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │               │               │
       └───────────────┼───────────────┘
                       ▼
                Research Merge
                       │
                       ▼
                   Analyst
                       │
                       ▼
                 Feasibility
                       │
                       ▼
                     Critic
                       │
             ┌─────────┴─────────┐
             │                   │
           REVISE                PASS
             │                   │
             ▼                   ▼
          Analyst              Final
```

------------------------------------------------------------------------

# 🧩 Agents

  Agent                 Main Responsibility
  --------------------- ---------------------------------------------
  Supervisor            Understand and coordinate the research task
  Planner               Create the research plan
  Web Researcher        Search web sources
  Academic Researcher   Search academic information
  RAG Researcher        Search user documents
  Research Merge        Combine research streams
  Analyst               Analyze and synthesize evidence
  Feasibility           Evaluate project feasibility
  Critic                Review and request revisions
  Final Writer          Produce the final report

------------------------------------------------------------------------

# 📝 Input

The primary input is a natural-language research question.

## Simple Input

``` text
How can AI improve the education system in India?
```

## Technical Input

``` text
How can computer vision be used for automated
traffic management in smart cities?
```

## Project Idea

``` text
I want to build an AI system that detects crop
diseases using images. What technologies,
datasets, existing solutions and challenges
should I consider?
```

## ECE Project Example

``` text
Can AI be used to automatically detect faults
in electronic circuits?
```

------------------------------------------------------------------------

# 📤 Output

The intended final output is a structured research report containing
sections such as:

``` text
Research Question

1. Executive Summary

2. Problem Understanding

3. Existing Solutions

4. Research Findings

5. Technical Approaches

6. Dataset Availability

7. Technology Comparison

8. Recommended Approach

9. Feasibility

10. Major Challenges

11. Research Gaps

12. Project Opportunities
```

The exact output depends on the research question and the available
evidence.

------------------------------------------------------------------------

# 🎬 Example Demo

## Input

``` text
How can AI improve the education system in India?
```

## Internal Processing

``` text
Supervisor
    ↓
Understands the research objective

Planner
    ↓
Creates research tasks

Web Researcher
    ↓
Finds current web information

Academic Researcher
    ↓
Finds academic research

RAG Researcher
    ↓
Searches uploaded documents, if available

Research Merge
    ↓
Combines findings

Analyst
    ↓
Synthesizes research

Feasibility
    ↓
Evaluates implementation

Critic
    ↓
Reviews the result

Revision
    ↓
Improves analysis if necessary
```

## Example Output

``` text
RESEARCH REPORT
===============

Research Question:
How can AI improve the education system in India?

Executive Summary:
AI can potentially support education through
personalized learning, intelligent tutoring,
automated assessment and teacher assistance.

Problem Understanding:
- Different learning levels
- Teacher workload
- Language diversity
- Unequal access
- Resource limitations

Existing Solutions:
- Intelligent tutoring systems
- Adaptive learning
- AI-based assessment
- AI teaching assistants

Technical Approaches:
- LLMs
- RAG
- Recommendation systems
- NLP
- Machine learning

Challenges:
- Data privacy
- Model reliability
- Language diversity
- Dataset quality
- Infrastructure

Research Gaps:
...

Recommended Project:
...

Feasibility:
...

Project Opportunities:
...
```

> The example above illustrates the expected report structure. Actual
> claims should come from the sources and documents processed by the
> running system.

------------------------------------------------------------------------

# 🖥️ Frontend

The frontend is built using:

-   React
-   Vite
-   CSS
-   JavaScript

The main interface provides:

``` text
ResearchForge AI
       │
       ├── Research Question
       │
       ├── Start Research
       │
       ├── Agent Status
       │
       └── Research Result
```

Frontend URL during development:

``` text
http://localhost:5173/
```

------------------------------------------------------------------------

# ⚙️ Backend

The backend is built using:

-   Python
-   FastAPI
-   LangChain
-   LangGraph
-   Mistral AI
-   Chroma
-   Tavily
-   Academic search services

Backend URL during development:

``` text
http://127.0.0.1:8000/
```

FastAPI documentation:

``` text
http://127.0.0.1:8000/docs
```

------------------------------------------------------------------------

# 🛠️ Technology Stack

## Frontend

``` text
React
Vite
JavaScript
CSS
```

## Backend

``` text
Python
FastAPI
```

## AI / LLM

``` text
Mistral AI
LangChain
LangGraph
```

## RAG

``` text
Embeddings
Chroma
Document Loaders
Text Splitters
Retriever
```

## Research

``` text
Tavily Web Search
Academic Search
User Documents
```

## Database

``` text
PostgreSQL
```

PostgreSQL is planned/used as the persistent application database layer
for project data as the application is expanded.

------------------------------------------------------------------------

# 📁 Project Structure

A representative project structure is:

``` text
researchforge-ai/
│
├── backend/
│   │
│   ├── main.py
│   │
│   ├── agents/
│   │   ├── supervisor.py
│   │   ├── planner.py
│   │   ├── web_researcher.py
│   │   ├── academic_researcher.py
│   │   ├── rag_researcher.py
│   │   ├── research_merge.py
│   │   ├── analyst.py
│   │   ├── feasibility.py
│   │   └── critic.py
│   │
│   ├── graph/
│   │   ├── state.py
│   │   ├── nodes.py
│   │   └── workflow.py
│   │
│   ├── llm/
│   │   └── models.py
│   │
│   ├── rag/
│   │   ├── loaders.py
│   │   ├── embeddings.py
│   │   ├── vectorstore.py
│   │   └── retriever.py
│   │
│   └── ...
│
├── frontend/
│   │
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

------------------------------------------------------------------------

# 📋 Prerequisites

Install the following:

### Python

Recommended:

``` text
Python 3.11+
```

Check:

``` powershell
python --version
```

### Node.js

Check:

``` powershell
node --version
npm --version
```

### Git

Check:

``` powershell
git --version
```

------------------------------------------------------------------------

# 🔐 Environment Variables

Create a `.env` file in the project root.

Example:

``` env
MISTRAL_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key
```

If your RAG embedding provider requires a separate API key, configure it
according to the embedding implementation.

### Important

Never commit `.env` to GitHub.

Add:

``` text
.env
```

to `.gitignore`.

------------------------------------------------------------------------

# 🐍 Backend Setup

From the project root:

``` powershell
cd E:\jeet\coding\project\researchforge-ai
```

Create a virtual environment:

``` powershell
python -m venv .venv
```

Activate it on Windows PowerShell:

``` powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

``` powershell
pip install -r requirements.txt
```

If you do not yet have a requirements file, install the project's
required packages according to the imports used by your backend.

------------------------------------------------------------------------

# ▶️ Start Backend

From the project root:

``` powershell
uvicorn backend.main:app --reload
```

Expected:

``` text
Uvicorn running on http://127.0.0.1:8000
Application startup complete.
```

Test:

``` text
http://127.0.0.1:8000/
```

Then open:

``` text
http://127.0.0.1:8000/docs
```

------------------------------------------------------------------------

# ⚛️ Frontend Setup

Open another terminal.

Go to:

``` powershell
cd E:\jeet\coding\project\researchforge-ai\frontend
```

Install dependencies:

``` powershell
npm install
```

Start Vite:

``` powershell
npm run dev
```

Expected:

``` text
Local: http://localhost:5173/
```

Open:

``` text
http://localhost:5173/
```

------------------------------------------------------------------------

# ▶️ Running the Complete Project

You need two terminals.

## Terminal 1 --- Backend

``` powershell
cd E:\jeet\coding\project\researchforge-ai

.venv\Scripts\Activate.ps1

uvicorn backend.main:app --reload
```

## Terminal 2 --- Frontend

``` powershell
cd E:\jeet\coding\project\researchforge-ai\frontend

npm run dev
```

Then open:

``` text
http://localhost:5173/
```

------------------------------------------------------------------------

# 🔌 API

The frontend communicates with the FastAPI backend.

Conceptual request:

``` http
POST /research
Content-Type: application/json
```

Request body:

``` json
{
  "user_query": "How can AI improve the education system in India?"
}
```

The final API response should contain the generated research
information.

A simple development/test response may look like:

``` json
{
  "status": "success",
  "user_query": "How can AI improve the education system in India?"
}
```

As the LangGraph integration is connected to the API, this response
should be expanded to include the workflow's final research report and
relevant metadata.

------------------------------------------------------------------------

# 📄 RAG Pipeline

ResearchForge AI uses Retrieval-Augmented Generation to ground analysis
in user-provided documents.

## Step 1 --- Load

``` text
PDF
 ↓
Document Loader
```

## Step 2 --- Split

``` text
Large Document
 ↓
Chunks
```

A recursive text splitter can divide the document into manageable
chunks.

## Step 3 --- Embed

``` text
Text Chunk
 ↓
Embedding Vector
```

## Step 4 --- Store

``` text
Embedding
 ↓
Chroma
```

## Step 5 --- Retrieve

When the user asks a question:

``` text
Question
 ↓
Query Embedding
 ↓
Chroma Search
 ↓
Relevant Chunks
```

## Step 6 --- Generate

The relevant chunks are passed to the RAG agent/LLM for grounded
analysis.

------------------------------------------------------------------------

# 🕸️ LangGraph Workflow

The workflow is represented as a graph rather than a simple linear
function.

Core nodes:

``` text
supervisor
planner
web_research
academic_research
rag_research
research_merge
analyst
feasibility
critic
```

Conceptually:

``` text
START
  ↓
Supervisor
  ↓
Planner
  ├──────────────┐
  ↓              ↓
Web            Academic
  ↓              ↓
  └───────┬──────┘
          ↓
         RAG
          ↓
    Research Merge
          ↓
       Analyst
          ↓
     Feasibility
          ↓
        Critic
          ↓
    Conditional Edge
       ↙        ↘
   REVISE       PASS
      ↓           ↓
   Analyst       END
```

------------------------------------------------------------------------

# 🔁 Revision Logic

The Critic returns a verdict.

Example:

``` text
VERDICT: REVISE
```

The workflow can return to the Analyst.

A revision counter prevents unlimited iterations.

Conceptually:

``` python
if revision_count >= 2:
    finish()

elif "VERDICT: REVISE" in critique:
    return "analyst"

else:
    finish()
```

This creates controlled iterative reasoning.

------------------------------------------------------------------------

# 🧪 Mock LLM Mode

External LLM APIs can sometimes return:

``` text
429 Too Many Requests
```

because of rate limits or temporary provider restrictions.

For development and workflow testing, a mock LLM can be used.

This allows you to test:

``` text
Graph construction
        ↓
Node execution
        ↓
Conditional routing
        ↓
Revision logic
```

without making every test dependent on live LLM calls.

For final demonstrations, use the real LLM when API availability and
limits allow it.

------------------------------------------------------------------------

# 🎯 Demo Scenarios

## Demo 1 --- AI in Education

Input:

``` text
How can AI improve the education system in India?
```

Expected areas:

``` text
Existing solutions
AI tutoring
Personalized learning
Datasets
Technology choices
Challenges
Research gaps
Project ideas
```

------------------------------------------------------------------------

## Demo 2 --- Healthcare

Input:

``` text
How can AI agents improve healthcare diagnostics?
```

Expected areas:

``` text
Existing approaches
AI technologies
Medical datasets
Research papers
Implementation challenges
Privacy concerns
Feasibility
Research gaps
```

------------------------------------------------------------------------

## Demo 3 --- Smart Cities

Input:

``` text
How can computer vision improve traffic management
in Indian cities?
```

Expected areas:

``` text
Computer vision methods
Traffic detection
Existing systems
Datasets
Infrastructure
Challenges
Recommended architecture
```

------------------------------------------------------------------------

## Demo 4 --- ECE / Circuit Troubleshooting

Input:

``` text
Can AI be used to automatically detect faults
in electronic circuits?
```

Expected areas:

``` text
Fault types
Existing diagnostic methods
Machine learning approaches
Datasets
Sensor requirements
Hardware/software architecture
Feasibility
Research gaps
```

------------------------------------------------------------------------

# 🧪 Recommended Demo for SIH / Hackathon

For a live demonstration, use a question that clearly shows the value of
multi-agent research.

Example:

``` text
I want to build an AI-based system that helps
students identify their learning gaps and provides
personalized learning recommendations.

Find existing solutions, research papers,
technologies, datasets, implementation challenges,
research gaps and recommend a feasible architecture.
```

This demonstrates:

``` text
Web Research
      +
Academic Research
      +
RAG
      +
Analysis
      +
Feasibility
      +
Critic
      =
Research Intelligence
```

------------------------------------------------------------------------

# 🐛 Troubleshooting

## 1. Frontend does not start

Run:

``` powershell
cd frontend
npm install
npm run dev
```

Then open:

``` text
http://localhost:5173/
```

------------------------------------------------------------------------

## 2. Backend does not start

Check:

``` text
backend/main.py
```

Then run from the project root:

``` powershell
uvicorn backend.main:app --reload
```

If you see:

``` text
Could not import module "backend.main"
```

verify that:

``` text
backend/
├── __init__.py
└── main.py
```

exists.

------------------------------------------------------------------------

## 3. CORS error

The backend should allow the frontend origin:

``` text
http://localhost:5173
```

Example:

``` python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Restart FastAPI after changing this configuration.

------------------------------------------------------------------------

## 4. Mistral 401 error

Check:

``` env
MISTRAL_API_KEY=your_real_key
```

Make sure the `.env` file is loaded and the key is valid.

------------------------------------------------------------------------

## 5. Mistral 429 error

A 429 generally indicates a provider-side rate limit or usage
restriction.

Possible development solutions:

-   Wait and retry.
-   Reduce request frequency.
-   Use mock LLM mode for graph testing.
-   Check provider usage/limits.
-   Avoid sending unnecessary repeated requests.

------------------------------------------------------------------------

## 6. Tavily API error

Check:

``` env
TAVILY_API_KEY=your_real_key
```

and restart the backend.

------------------------------------------------------------------------

## 7. Browser says backend cannot connect

Check:

``` text
http://127.0.0.1:8000/
```

If it works, check:

``` text
http://127.0.0.1:8000/docs
```

Then check the browser developer console for CORS or endpoint errors.

------------------------------------------------------------------------

# 🔐 Security

Do not commit secrets.

Never push:

``` text
.env
API keys
tokens
passwords
database credentials
```

Use:

``` text
.env
```

and add it to `.gitignore`.

For production:

-   Use environment variables/secrets management.
-   Add authentication.
-   Validate API input.
-   Add request limits.
-   Secure database credentials.
-   Restrict CORS origins.
-   Add logging without exposing secrets.

------------------------------------------------------------------------

# 🚀 Future Improvements

Potential future features include:

### Authentication

``` text
Login
Signup
User Profiles
```

### Project Management

``` text
Create Research Project
Save Research
Update Research
Delete Research
```

### Document Management

``` text
Upload PDF
Upload DOCX
Document Library
Document-specific RAG
```

### Research History

``` text
Previous Research
Saved Reports
Search History
```

### Report Export

``` text
PDF
DOCX
Markdown
```

### Better Source Management

``` text
Source citations
Source ranking
Source credibility scoring
```

### Advanced Agent Monitoring

``` text
Supervisor     ✓
Planner        ✓
Web Research   ✓
Academic       ✓
RAG            ✓
Analyst        ✓
Feasibility    ✓
Critic         ✓
```

### PostgreSQL Integration

Store:

``` text
Users
Projects
Research Questions
Research Reports
Documents
Research History
Agent Metadata
```

### Production Deployment

Possible deployment architecture:

``` text
React
  ↓
Cloud Frontend
  ↓
FastAPI
  ↓
LangGraph
  ↓
LLM / Search / Vector DB
  ↓
PostgreSQL
```

------------------------------------------------------------------------

# 🎓 Interview / Viva Explanation

## What is ResearchForge AI?

> ResearchForge AI is a multi-agent AI research platform that takes a
> research question or project idea and uses specialized agents for
> planning, web research, academic research, document retrieval,
> analysis, feasibility evaluation and critical review to generate a
> structured research report.

------------------------------------------------------------------------

## Why use multiple agents?

> Different research tasks require different responsibilities. Instead
> of using one LLM for everything, ResearchForge assigns specialized
> roles to agents. This makes the workflow modular, easier to control,
> and easier to extend.

------------------------------------------------------------------------

## Why LangGraph?

> LangGraph allows us to represent the research process as a stateful
> graph. It supports multiple nodes, branching, conditional routing and
> iterative loops, which are useful for coordinating multiple research
> agents and implementing the Critic revision cycle.

------------------------------------------------------------------------

## Why RAG?

> RAG allows the system to retrieve relevant information from
> user-provided documents before generating an answer. This helps the
> system incorporate private or project-specific knowledge instead of
> relying only on the model's internal knowledge.

------------------------------------------------------------------------

## Why a Critic Agent?

> The Critic evaluates the research produced by previous agents. If
> important weaknesses are found, it can request another analysis
> iteration. This creates a controlled self-review mechanism.

------------------------------------------------------------------------

## What makes the project different from a normal chatbot?

A normal chatbot:

``` text
User
 ↓
LLM
 ↓
Answer
```

ResearchForge AI:

``` text
User
 ↓
Supervisor
 ↓
Planner
 ↓
Multiple Research Agents
 ↓
Research Merge
 ↓
Analyst
 ↓
Feasibility
 ↓
Critic
 ↓
Revision
 ↓
Final Research
```

The main value is the **structured research workflow**, not simply
generating text.

------------------------------------------------------------------------

# 📊 Project Highlights

``` text
✓ Multi-Agent Architecture
✓ LangGraph Workflow
✓ LangChain Integration
✓ Mistral LLM
✓ Web Research
✓ Academic Research
✓ RAG
✓ Chroma Vector Database
✓ Research Merging
✓ Structured Analysis
✓ Feasibility Evaluation
✓ Critic Agent
✓ Conditional Revision Loop
✓ FastAPI Backend
✓ React + Vite Frontend
✓ Mock LLM Support
✓ Extensible Architecture
```

------------------------------------------------------------------------

# 🏗️ Development Status

The project is being developed incrementally.

### Core AI / Backend

``` text
LLM Setup                 ✓
RAG                       ✓
Web Search                ✓
Academic Research         ✓
Supervisor Agent          ✓
Planner Agent             ✓
Web Research Agent        ✓
Academic Agent            ✓
RAG Agent                 ✓
Research Merge            ✓
Analyst                   ✓
Feasibility               ✓
Critic                    ✓
LangGraph Workflow        ✓
Revision Loop             ✓
Mock Workflow Testing     ✓
```

### Frontend

``` text
React + Vite Setup        ✓
Research UI               ✓
Agent UI                  ✓
Result UI                 ✓
Backend Connection        In Progress
Full Graph Result UI      In Progress
```

### Planned Application Features

``` text
Authentication             Planned
Project Management         Planned
Document Upload UI         Planned
Research History           Planned
Report Export              Planned
PostgreSQL Persistence     Planned
Production Deployment     Planned
```

------------------------------------------------------------------------

# 🤝 Contributing

Contributions are welcome.

General workflow:

``` bash
git clone <repository-url>

cd researchforge-ai

git checkout -b feature/your-feature

# Make changes

git add .

git commit -m "Add your feature"

git push origin feature/your-feature
```

Then open a Pull Request.

------------------------------------------------------------------------

# 📄 License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

------------------------------------------------------------------------

# 👨‍💻 Author

**Jeet Gondaliya**

ResearchForge AI --- Multi-Agent AI Research Platform

------------------------------------------------------------------------

# ⭐ Final Summary

ResearchForge AI can be summarized as:

``` text
                RESEARCHFORGE AI
                       │
                       ▼
                Research Question
                       │
                       ▼
                  Supervisor
                       │
                       ▼
                    Planner
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
       Web          Academic          RAG
    Research       Research        Documents
        │              │              │
        └──────────────┼──────────────┘
                       ▼
                 Research Merge
                       │
                       ▼
                    Analyst
                       │
                       ▼
                  Feasibility
                       │
                       ▼
                     Critic
                       │
              ┌────────┴────────┐
              ▼                 ▼
           REVISE              PASS
              │                 │
              └──→ Analyst      ▼
                             Final
                             Report
```

> **ResearchForge AI turns a research question into a structured
> research process using multiple specialized AI agents.**
