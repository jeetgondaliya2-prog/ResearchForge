from langchain_core.messages import HumanMessage
from backend.llm.models import get_llm
from backend.tools.calculator import calculator
from backend.tools.document_search import document_search


def create_research_agent():

    llm = get_llm()

    tools = [
        calculator,
        document_search
    ]

    llm_with_tools = llm.bind_tools(tools)

    return llm_with_tools