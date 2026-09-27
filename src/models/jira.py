from pydantic import BaseModel, Field


class JiraTicket(BaseModel):
    """Structured Jira engagement proposal."""

    it_component: str = Field(
        description="The impacted IT component."
    )

    jira_project: str = Field(
        description=(
            "The Jira project associated with the IT component. "
        )
    )

    summary: str = Field(
        description="A concise summary for the Jira engagement."
    )

    description: str = Field(
        description=(
            "The complete Jira description containing the required "
            "Benefit/Value, Work Required, Dependencies, and "
            "Definition of Done sections."
        )
    )

    delivery_team: str = Field(
        description="The delivery team responsible for the Jira engagement."
    )

    labels: list[str] = Field(
        description=(
            "Jira labels containing the PI planning quarter, "
            "Navigator ID, and Domain."
        )
    )

    dependencies: list[str] = Field(
        default_factory=list,
        description="Dependencies identified from the source information."
    )

    definition_of_done: list[str] = Field(
        default_factory=list,
        description=(
            "Definition of Done derived from the Confluence "
            "acceptance criteria."
        )
    )

    acceptance_criteria: list[str] = Field(

        default_factory=list,
        description=(
            "Acceptance criteria derived from the Confluence "
            "documentation."
        )
    )

class ReturnJiraTicket(BaseModel):
    """
    Pydantic model for the jira ticket create and returned by the Jira tool.
    """

    jira_key: str = Field(description="The Jira ticket key, e.g., 'MOCK-IT-COMPONENT-001'.")
    jira_url: str = Field(description="The URL to the Jira ticket, e.g., 'https://jira.example.com/browse/MOCK-IT-COMPONENT-001'.")
    it_component: str = Field(description="The impacted IT component.")
    jira_project: str = Field(description="The Jira project associated with the IT component.")
    description: str = Field(description="""The complete Jira description containing the required
                Benefit/Value, Work Required, Dependencies, and 
                Definition of Done sections.""")
    delivery_team: str = Field(description="The delivery team responsible for the Jira engagement.")

class CreatedJiraTickets(BaseModel):
    """
    Result returned after creating a batch of Jira tickets.
    """
    status: str = Field(
        description="Creation status, for example 'success'."
    )

    created_tickets: list[ReturnJiraTicket] = Field(
        description="The Jira tickets created by the batch operation."
    )

class ComponentMatch(BaseModel):
    input_component: str = Field(
        description="IT component extracted from the Confluence page."
    )

    match_found: bool = Field(
        description= (
            "True if there is a match found else False"
        )
    )

    matched_component: str | None = Field(
        description=(
            "The IT_Component from the registry that best matches "
            "the input component. Null if no reliable match exists."
        )
    )

    project_jira: str | None = Field(
        description=(
            "The Jira project associated with the matched IT_Component. "
            "Null if no reliable match exists."
        )
    )

    delivery_team: str | None = Field(
        description=(
            "The delivery team associated with the matched IT_Component. "
            "Null if no reliable match exists."
        )
    )
    confidence: float = Field(
        description="Confidence of the component match between 0 and 1."
    )

    reason: str = Field(
        description="Brief explanation for the selected match."
    )

class ComponentResolutionResult(BaseModel):
    matches: list[ComponentMatch]= Field(
        description="Component matching results."
    )