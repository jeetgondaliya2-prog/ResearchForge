import os

from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage


load_dotenv()


class MockLLM:
    """
    Mock LLM for development / workflow testing without live API calls.
    Returns a structured 15-section markdown report so the frontend
    parseSections() function can render it correctly.
    """

    def invoke(self, prompt: str) -> AIMessage:

        print("[MOCK LLM] Simulating LLM response...")

        # Detect which agent is calling based on prompt keywords
        p = prompt.lower()

        if "supervisor" in p and "coordinate" in p:
            return AIMessage(content=(
                "This research request requires:\n"
                "1. Web research — to find current solutions and industry applications.\n"
                "2. Academic research — to discover peer-reviewed papers.\n"
                "3. RAG research — to search user-uploaded documents.\n"
                "4. Technical analysis — to compare approaches.\n"
                "5. Feasibility analysis — to evaluate project buildability."
            ))

        if "planning agent" in p or "break this request" in p:
            return AIMessage(content=(
                "1. Search for existing AI solutions and tools\n"
                "2. Find relevant academic research papers\n"
                "3. Identify available datasets\n"
                "4. Analyze technical implementation approaches\n"
                "5. Evaluate limitations and challenges\n"
                "6. Identify research gaps and opportunities"
            ))

        if "web research agent" in p:
            return AIMessage(content=(
                "Web Research Findings:\n\n"
                "1. Important Findings:\n"
                "   - Multiple established solutions exist in this domain.\n"
                "   - Industry adoption is growing rapidly.\n\n"
                "2. Existing Solutions:\n"
                "   - OpenAI GPT-4 based systems\n"
                "   - Google Vertex AI pipelines\n"
                "   - Open-source LangChain-based frameworks\n\n"
                "3. Current Technologies:\n"
                "   - Large Language Models (LLMs)\n"
                "   - Retrieval-Augmented Generation (RAG)\n"
                "   - Vector databases (ChromaDB, Pinecone, Weaviate)\n\n"
                "4. Research Gaps:\n"
                "   - Limited solutions for low-resource domains.\n"
                "   - Evaluation benchmarks are inconsistent.\n"
                "   - Privacy-preserving approaches are underexplored."
            ))

        if "academic research agent" in p:
            return AIMessage(content=(
                "Academic Research Findings:\n\n"
                "1. Key Research Papers Found:\n"
                "   - 'Attention Is All You Need' (Vaswani et al., 2017)\n"
                "   - 'RAG for Knowledge-Intensive NLP Tasks' (Lewis et al., 2020)\n"
                "   - 'Chain-of-Thought Prompting' (Wei et al., 2022)\n\n"
                "2. Algorithms & Models:\n"
                "   - Transformer architecture\n"
                "   - Dense passage retrieval (DPR)\n"
                "   - Multi-agent orchestration frameworks\n\n"
                "3. Datasets Used in Literature:\n"
                "   - Natural Questions (NQ)\n"
                "   - TriviaQA\n"
                "   - MS MARCO\n\n"
                "4. Research Gaps:\n"
                "   - Multi-hop reasoning remains challenging.\n"
                "   - Domain adaptation requires more work.\n"
                "   - Hallucination reduction is an open problem."
            ))

        if "rag research agent" in p:
            return AIMessage(content=(
                "RAG Document Research:\n\n"
                "No user documents were uploaded for this session. "
                "The RAG Researcher could not find relevant information in uploaded documents. "
                "Upload PDF or DOCX files via the Documents section to include private knowledge in the research."
            ))

        if "analyst agent" in p or "combine all available research" in p:
            return AIMessage(content=(
                "Research Analysis:\n\n"
                "1. Problem Understanding:\n"
                "The research question involves a complex sociotechnical challenge "
                "requiring a combination of AI, data engineering, and domain expertise.\n\n"
                "2. Existing Solutions:\n"
                "Several established solutions exist, including LLM-based pipelines, "
                "RAG systems, and specialized ML models. Each approach has trade-offs.\n\n"
                "3. Research Findings:\n"
                "Academic literature confirms the importance of grounded retrieval to "
                "reduce hallucination. Industry solutions favor hybrid approaches.\n\n"
                "4. Technical Approaches:\n"
                "- RAG with dense retrieval\n"
                "- Fine-tuned domain models\n"
                "- Multi-agent orchestration\n"
                "- Chain-of-thought prompting\n\n"
                "5. Dataset Availability:\n"
                "Publicly available datasets exist in most major domains. "
                "Custom dataset collection may be required for niche applications.\n\n"
                "6. Technology Comparison:\n"
                "- OpenAI GPT-4: High accuracy, expensive, closed source\n"
                "- Mistral: Good performance, cost-effective, open weights available\n"
                "- LLaMA 3: Open-source, strong community support\n\n"
                "7. Recommended Approach:\n"
                "A modular architecture combining RAG, LLM reasoning, and agent orchestration "
                "is recommended. Use Mistral for cost-efficiency.\n\n"
                "8. Major Challenges:\n"
                "- Hallucination risk\n"
                "- API rate limits\n"
                "- Evaluation difficulty\n"
                "- Data quality\n\n"
                "9. Research Gaps:\n"
                "- Automated evaluation of multi-agent outputs\n"
                "- Domain adaptation with minimal data\n"
                "- Privacy-preserving RAG\n\n"
                "10. Project Opportunities:\n"
                "Build a specialized research assistant that combines web, academic, "
                "and document research into a single structured workflow."
            ))

        if "feasibility agent" in p or "realistically buildable" in p:
            return AIMessage(content=(
                "Feasibility Evaluation:\n\n"
                "1. Technical Feasibility (Score: 8/10)\n"
                "The required technologies are mature and well-documented. "
                "LangChain, LangGraph, and Mistral AI provide solid foundations.\n\n"
                "2. Dataset Availability (Score: 7/10)\n"
                "Public datasets exist for most use cases. "
                "Domain-specific datasets may need to be collected.\n\n"
                "3. Required Hardware (Score: 9/10)\n"
                "Cloud APIs eliminate the need for GPU hardware in most scenarios.\n\n"
                "4. Required Software (Score: 9/10)\n"
                "Python, FastAPI, LangChain, LangGraph, ChromaDB — all free and open source.\n\n"
                "5. Model Complexity (Score: 7/10)\n"
                "Multi-agent orchestration is complex but manageable with LangGraph.\n\n"
                "6. Development Difficulty (Score: 6/10)\n"
                "Moderate complexity. Requires knowledge of LLMs and API integration.\n\n"
                "7. Development Stages (Score: 8/10)\n"
                "Stage 1: Core agents → Stage 2: RAG → Stage 3: Frontend → Stage 4: Deployment\n\n"
                "8. Major Risks (Score: 6/10)\n"
                "- LLM API rate limits\n"
                "- Hallucination in generated reports\n"
                "- Cost at scale\n\n"
                "9. Cost Considerations (Score: 8/10)\n"
                "Mistral API is cost-effective. ChromaDB is free. Infrastructure costs are low.\n\n"
                "10. Expected Performance (Score: 7/10)\n"
                "Good quality research reports with real API calls. Mock mode for testing.\n\n"
                "11. Scalability (Score: 7/10)\n"
                "Can scale with async processing and queue-based architecture.\n\n"
                "12. Future Improvements (Score: 9/10)\n"
                "Authentication, PostgreSQL persistence, report export, streaming responses.\n\n"
                "OVERALL FEASIBILITY: HIGH\n\n"
                "This project is technically sound and buildable with the current technology stack."
            ))

        if "critic agent" in p or "critically evaluate" in p:
            return AIMessage(content=(
                "Critic Review:\n\n"
                "The analysis provides a solid foundation with clear structure.\n\n"
                "Strengths:\n"
                "- Comprehensive coverage of existing solutions\n"
                "- Clear technical approach recommendations\n"
                "- Realistic feasibility assessment\n\n"
                "Weaknesses:\n"
                "- Dataset citations could be more specific\n"
                "- Privacy considerations need more depth\n"
                "- Cost estimates are general\n\n"
                "VERDICT: PASS\n\n"
                "The analysis meets the required quality threshold. "
                "The research is well-structured and provides actionable insights."
            ))

        if "final writer" in p or "professional research" in p or "executive summary" in p:
            return AIMessage(content=self._mock_final_report(prompt))

        # Generic fallback
        return AIMessage(content=(
            "Analysis completed. The research provides useful insights into the topic. "
            "Multiple approaches were identified with varying trade-offs in complexity, "
            "cost, and performance. A modular architecture is recommended."
        ))

    def _mock_final_report(self, prompt: str) -> str:
        # Extract the research question from the prompt if possible
        query_hint = "the research topic"
        lines = prompt.split("\n")
        for i, line in enumerate(lines):
            if "RESEARCH QUESTION" in line and i + 2 < len(lines):
                q = lines[i + 2].strip()
                if q:
                    query_hint = q
                break

        return f"""# ResearchForge AI Research Report

## 1. Executive Summary

This report addresses the research question: **{query_hint}**

AI-powered multi-agent research systems can transform how we approach complex research questions by combining web search, academic literature, and document retrieval into a single structured workflow. The key finding is that a modular, RAG-augmented LLM pipeline offers the best balance of accuracy, cost, and scalability.

## 2. Problem Definition

The core challenge involves automating research synthesis across multiple information sources — web, academic papers, and private documents — while maintaining factual accuracy and producing actionable insights. Traditional manual research is slow, fragmented, and difficult to scale.

## 3. Existing Solutions

Several platforms and tools exist in this space:

- **LangChain** — Framework for building LLM-powered applications
- **LlamaIndex** — Specialized in document retrieval and RAG pipelines
- **AutoGPT / CrewAI** — Multi-agent autonomous research frameworks
- **Perplexity AI** — Web-search-augmented answer engine
- **Elicit** — AI research assistant for academic literature

Each solution has trade-offs in cost, accuracy, extensibility, and transparency.

## 4. Research Findings

Key findings from academic and web research:

- Retrieval-Augmented Generation (RAG) significantly reduces hallucination compared to pure LLM inference
- Multi-agent systems outperform single-agent systems on complex tasks requiring diverse expertise
- Chain-of-thought prompting improves reasoning quality in structured analysis tasks
- Critic-revision loops (self-reflection) improve output quality in agentic systems
- Open-source models like Mistral are increasingly competitive with proprietary alternatives

## 5. Technical Approaches

The following technical approaches are relevant:

- **RAG Pipeline** — Embed documents → Store in ChromaDB → Retrieve relevant chunks → LLM synthesis
- **Multi-Agent Orchestration** — LangGraph StateGraph with conditional routing and revision loops
- **Web Search Integration** — Tavily API for real-time internet search
- **Academic Search** — arXiv API for peer-reviewed research discovery
- **LLM Integration** — Mistral AI for cost-effective, high-quality language model inference

## 6. Dataset Analysis

Publicly available datasets relevant to this domain:

- **Natural Questions (NQ)** — 300K question-answer pairs from Google Search
- **MS MARCO** — 1M queries with passage-level annotations
- **arXiv Dataset** — 1.7M academic papers across STEM domains
- **Common Crawl** — Web-scale text data for pre-training
- **Custom Domain Datasets** — May need to be collected for specialized applications

## 7. Technology Comparison

| Technology | Accuracy | Cost | Open Source | Scalability |
|---|---|---|---|---|
| GPT-4 | Very High | High | No | High |
| Mistral | High | Low | Partial | High |
| LLaMA 3 | High | Free | Yes | Medium |
| ChromaDB | — | Free | Yes | Medium |
| Pinecone | — | Medium | No | Very High |

## 8. Recommended Architecture

The recommended system architecture for this research problem:

```
User Query
    ↓
Supervisor Agent (LangGraph)
    ↓
Planner Agent
    ↓
[Web Research] + [Academic Research] + [RAG Research]
    ↓
Research Merge
    ↓
Analyst Agent → Feasibility Agent → Critic Agent
    ↓ (conditional revision loop)
Final Writer Agent
    ↓
Structured Research Report
```

**Technology Stack:** Python · FastAPI · LangGraph · LangChain · Mistral AI · ChromaDB · Tavily · arXiv

## 9. Implementation Plan

A practical implementation roadmap:

1. **Phase 1 (Week 1-2):** Set up core infrastructure — FastAPI backend, LangGraph workflow, Mistral LLM integration
2. **Phase 2 (Week 3-4):** Implement research agents — Web Researcher, Academic Researcher, RAG Researcher
3. **Phase 3 (Week 5-6):** Implement analysis agents — Analyst, Feasibility, Critic with revision loop
4. **Phase 4 (Week 7-8):** Build React frontend — Research input, live pipeline, report viewer
5. **Phase 5 (Week 9-10):** Add persistence — document upload, research history, report export
6. **Phase 6 (Week 11-12):** Testing, optimization, and deployment

## 10. Feasibility

- **Technical Feasibility:** HIGH — All required technologies are mature and well-documented
- **Dataset Feasibility:** HIGH — Public datasets available; custom data collection manageable
- **Cost:** LOW to MEDIUM — Mistral API is affordable; ChromaDB and arXiv are free
- **Complexity:** MEDIUM — Multi-agent orchestration adds complexity but LangGraph handles it well
- **Deployment Feasibility:** HIGH — Standard cloud deployment with Docker and FastAPI

## 11. Challenges

Major challenges to address:

- **LLM Hallucination** — Agents may generate plausible but incorrect information
- **API Rate Limits** — Mistral and Tavily impose request limits; need retry logic
- **Context Window** — Large research compilations may exceed LLM context limits
- **Evaluation Difficulty** — Automated quality assessment of research reports is hard
- **Latency** — Multi-agent pipelines with real LLM calls take 30-120 seconds

## 12. Research Gaps

Areas where existing solutions are insufficient:

- **Automated evaluation metrics** for multi-agent research quality
- **Privacy-preserving RAG** for sensitive enterprise documents
- **Cross-lingual research** synthesis across multiple languages
- **Domain adaptation** with minimal labeled examples
- **Real-time knowledge updates** without full vector store re-indexing

## 13. Project Opportunities

Practical project ideas arising from this research:

1. **Domain-Specific Research Assistant** — A specialized version for healthcare, legal, or finance
2. **Research Paper Summarizer** — Batch processing of academic literature with trend identification
3. **Competitive Intelligence Platform** — Automated market research using web and document sources
4. **Student Research Helper** — Academic paper discovery and structured literature review
5. **Patent Analysis Tool** — Prior art search and novelty assessment for inventors

## 14. Future Improvements

Possible extensions and improvements:

- **Streaming responses** — Show intermediate agent outputs in real-time via WebSockets
- **PostgreSQL persistence** — Store research history, user sessions, and saved reports
- **Authentication** — User login, profiles, and personalized research history
- **Report Export** — PDF, DOCX, and Markdown export of generated reports
- **Collaborative Research** — Multi-user shared research sessions
- **Citation Management** — Automatic BibTeX/APA reference generation
- **Agent Monitoring Dashboard** — Real-time visualization of the LangGraph workflow

## 15. Final Recommendation

**ResearchForge AI demonstrates that a well-architected multi-agent system can significantly automate and improve the research process.**

The recommended approach is to build a modular LangGraph-based pipeline using:
- **Mistral AI** for cost-effective LLM reasoning
- **Tavily** for real-time web search
- **arXiv API** for academic research discovery
- **ChromaDB** for document-grounded RAG retrieval
- **FastAPI + React** for the full-stack application

This architecture is technically feasible, cost-effective, and extensible. The conditional Critic revision loop provides quality control, and the 15-section structured report format ensures comprehensive coverage of all research dimensions.

**Start with a focused prototype and expand incrementally. The foundation is solid.**
"""


def get_llm():

    mock_mode = os.getenv("MOCK_LLM", "false").lower() == "true"

    if mock_mode:

        print("[INFO] MOCK_LLM enabled — using MockLLM")

        return MockLLM()

    return ChatMistralAI(
        model="mistral-small-2506",
        temperature=0,
        api_key=os.getenv("MISTRAL_API_KEY")
    )