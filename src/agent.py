from pathlib import Path
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from tools.getskill import get_skill
from dotenv import load_dotenv
from tools.confluence import get_confluence_page, update_confluence_page
from tools.jira import validate_jira_structure, create_jira_tickets
from tools.component_resolver import resolve_components
from langchain.agents.middleware import HumanInTheLoopMiddleware

load_dotenv()


def get_checkpointer():
    """
    POC checkpointer.

    This is intentionally isolated so that we can later
    replace InMemorySaver with a database-backed solution.
    """
    return InMemorySaver()


def create_delivery_agent():

    model = ChatGoogleGenerativeAI(
                      model="gemini-3.7-flash",
                      temperature=1.0
                     )

    checkpointer = get_checkpointer()



    agent = create_agent(
        model=model,
        tools=[
            get_confluence_page,
            resolve_components,
            validate_jira_structure,
            create_jira_tickets,
            update_confluence_page,
            get_skill,
        ],
        system_prompt=(
            """You are a Delivery Engagement Assistant.
            Help Delivery Leads create IT component engagements.
            according to the business skill provided to you.
            
            You have access to specialized skills through the get_skill
tool.

When a user request requires specialized instructions:

1. Identify the required skill.
2. Call get_skill to load it.
3. Follow the loaded skill instructions.
4. Use the appropriate tools.
5. Never invent missing information.

"""
        ),
        middleware=[
            HumanInTheLoopMiddleware(
                interrupt_on={
                    "create_jira_tickets":{
                        "allowed_decisions": ["approve", "reject"],
                        "description": "The agent is requesting to create all proposed Jira tickets. Please review the complete batch of tickets and decide whether to approve, reject."
                    }
                }
            ),
        ],
        checkpointer=checkpointer,
    )

    return agent