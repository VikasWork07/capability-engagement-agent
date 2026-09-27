import json

from langchain.tools import tool
from pydantic import BaseModel, Field

from models.jira import (
    JiraTicket,
    ReturnJiraTicket,
    CreatedJiraTickets,
)






@tool
def validate_jira_structure(
    it_component: str,
    jira_project: str,
    summary: str,
    description: str,
    delivery_team: str,
    labels: list[str],
    dependencies: list[str],
    definition_of_done: list[str],
    acceptance_criteria: list[str],
) -> str:
    """
    Use this tool to validate the proposed Jira engagement structure. Does not create a Jira ticket.
    It only validates the proposed structure using the JiraTicket Pydantic model.
    """

    ticket = JiraTicket(
        it_component=it_component,
        jira_project=jira_project,
        summary=summary,
        description=description,
        delivery_team=delivery_team,
        labels=labels,
        dependencies=dependencies,
        definition_of_done=definition_of_done,
        acceptance_criteria=acceptance_criteria,
    )

    return ticket.model_dump_json(indent=2)


@tool
def create_jira_tickets(tickets: list[JiraTicket]) -> CreatedJiraTickets:
    """
    This creates JIRA tickets received as input.
    """

    created_tickets = []
    for ticket in tickets:
        print(f"Jira ticket: {ticket.model_dump_json(indent=2)}")
    
        
    # Temporary deterministic mock Jira reference.
        component_key = (
            ticket.it_component
            .upper()
            .replace(" ", "-")
            .replace("/", "-")
        )

        jira_key = f"MOCK-{component_key[:20]}-001"
        jira_url = (
            f"https://jira.example.com/browse/{jira_key}"
        )
        return_ticket = ReturnJiraTicket(
            jira_key=jira_key,
            jira_url=jira_url,
            it_component=component_key,
            jira_project=ticket.jira_project,
            description=ticket.description,
            delivery_team=ticket.delivery_team,
        )
        created_tickets.append(return_ticket)
    return CreatedJiraTickets(
        status="success",
        created_tickets=created_tickets
    )
