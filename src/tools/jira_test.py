from langchain.tools import tool

from models.jira import JiraTicket


@tool
def validate_jira_structure(
    it_component: str,
    jira_project: str,
    summary: str,
    description: str,
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
        labels=labels,
        dependencies=dependencies,
        definition_of_done=definition_of_done,
        acceptance_criteria=acceptance_criteria,
    )

    return ticket.model_dump_json(indent=2)


@tool
def create_jira_ticket(
    it_component: str,
    jira_project: str,
    summary: str,
    description: str,
    labels: list[str],
    dependencies: list[str],
    definition_of_done: list[str],
    acceptance_criteria: list[str],
) -> str:
    """
    This tool creates a JIRA engagement ticket on the JIRA platform/URL.
    """

    ticket = JiraTicket(
        it_component=it_component,
        jira_project=jira_project,
        summary=summary,
        description=description,
        labels=labels,
        dependencies=dependencies,
        definition_of_done=definition_of_done,
        acceptance_criteria=acceptance_criteria,
    )

    # Temporary deterministic mock Jira reference.
    component_key = (
        ticket.it_component
        .upper()
        .replace(" ", "-")
        .replace("/", "-")
    )

    fake_ticket_key = f"MOCK-{component_key[:20]}-001"
    fake_ticket_url = (
        f"https://jira.example.com/browse/{fake_ticket_key}"
    )

    return (
        "Mock Jira ticket created successfully.\n"
        f"Jira Key: {fake_ticket_key}\n"
        f"Jira URL: {fake_ticket_url}\n"
        f"IT Component: {ticket.it_component}\n"
        f"Jira Project: {ticket.jira_project}"
    )

