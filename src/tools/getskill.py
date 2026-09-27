from langchain.tools import tool

from skills import load_skill


@tool
def get_skill(skill_name: str) -> str:
    """
    Load the instructions for a specific skill.

    Use this tool when a task requires specialized instructions.
    Available skills include capability-engagement.
    """

    return load_skill(skill_name)