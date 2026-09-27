import csv

from langchain.tools import tool
from .jira import ReturnJiraTicket
from pathlib import Path

@tool
def get_confluence_page(url: str) -> str:
    """
    Retrieve the contents of a Confluence Engagement and Dependency page.

    Use this tool whenever the user provides a Confluence page URL
    and the task requires understanding the initiative, impacted
    IT components, work required, acceptance criteria, or dependencies.
    """

    # Temporary mock content for the POC.
    # This will be replaced with the real Confluence API later.

    return """
Initiative Name:
MPMP Loans

IT Capability:
ETL-FHC markers data ingestion to BFADS from relevant sources.
MPMP journey retrieves markers from BFADS to execute FHC eligibility checks and identify if the customer is eligible to access MPMP journey. ETL engine implements rules to source FHC markers data from respective source systems (SDM, BIW, Product platforms etc), and these markers are then ingested to BGADS for digital journey consumption.

Business/Customer Outcome:
1. Customer FHC markers ingested to BFADS for storage, maintenanca and audit purposes
2. Enables markers availability in BFADS for retrieval
3. Supports FHC checks for the MPMP journey eligibility

IT Component: ETL Data Pipe


Work Required:
1. ETL Development team: Implement ETL jobs with
    Source and Target system connections
    Data Extraction Logic from source systems
    Data Transformation (if applicable)
    Load process to BFADS
    Error handling and logging
2. Scheduling team: Schedule the ETL jobs to run at defined intervals
3. Monitoring team: Monitor the ETL jobs for successful execution and handle any failures or errors

Acceptance Criteria:
- ETL jobs successfully extract data from source systems.
- Data transformations produce correct results.
- Data is successfully loaded to BFADS.
- Job scheduling operates reliably.
- Error handling captures and logs any issues for troubleshooting.
- Job performance meets defined SLAs.

Dependencies:
- Data availability in source systems(SDM, BIW).
- Target system(BFADS) schema available to load the markers data


IT Component: Customer Data Platform

Impact / Change:
The Customer Data Platform needs to provide the customer
information required by the modernised lending journey.

Work Required:
Expose the required customer data through the agreed API.

Acceptance Criteria:
- Required customer data is available through the API.
- API meets the agreed response requirements.

Dependencies:
- Customer Data Platform API availability.
- Digital Lending platform integration.
"""


@tool
def update_confluence_page(
    page_url: str,
    jira_tickets: list[ReturnJiraTicket],
) -> str:
    """
    Update the Confluence engagement and dependency page with the
    Jira tickets created for the impacted IT components.
    """

    print("\n--- MOCK CONFLUENCE UPDATE ---")
    print(f"Page URL: {page_url}")

    output_dir = Path(__file__).parent.parent / "mock_confluence_updates"
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_file = output_dir / "jira_tickets.csv"
    fieldnames = [
        "it_component",
        "jira_project",
        "jira_key",
        "jira_url",
        "delivery_team",
        "description",
    ]
    with csv_file.open(mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for ticket in jira_tickets:
            writer.writerow(
                {
                    "it_component": ticket.it_component,
                    "jira_project": ticket.jira_project,
                    "jira_key": ticket.jira_key,
                    "jira_url": ticket.jira_url,
                    "delivery_team": ticket.delivery_team,
                    "description": ticket.description,
                }
            )

    return (
        "Mock Confluence page updated successfully.\n"
        f"Page URL: {page_url}\n"
        f"Jira tickets written back: {len(jira_tickets)}"
    )