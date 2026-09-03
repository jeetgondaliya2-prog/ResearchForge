from backend.agents.supervisor import supervisor_agent
from backend.agents.planner import planner_agent

from backend.agents.web_researcher import web_research_agent
from backend.agents.academic_researcher import academic_research_agent
from backend.agents.rag_researcher import rag_research_agent

from backend.agents.research_merge import research_merge_agent

from backend.agents.analyst import analyst_agent
from backend.agents.feasibility import feasibility_agent
from backend.agents.critic import critic_agent

from backend.agents.final_writer import final_writer_agent


def supervisor_node(state):
    return supervisor_agent(state)


def planner_node(state):
    return planner_agent(state)


def web_research_node(state):
    return web_research_agent(state)


def academic_research_node(state):
    return academic_research_agent(state)


def rag_research_node(state):
    return rag_research_agent(state)


def research_merge_node(state):
    return research_merge_agent(state)


def analyst_node(state):
    return analyst_agent(state)


def feasibility_node(state):
    return feasibility_agent(state)


def critic_node(state):
    return critic_agent(state)


def final_writer_node(state):
    return final_writer_agent(state)