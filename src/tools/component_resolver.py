import csv
from pathlib import Path

from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

from models.jira import ComponentResolutionResult, ComponentMatch
from typing import Annotated


CSV_FILE = (
    Path(__file__).resolve().parent.parent
    / "config"
    / "IT_registry.csv"
)


def load_component_registry() -> list[dict[str, str]]:
    """Load the complete component registry from CSV."""

    with CSV_FILE.open(
        mode="r",
        encoding="utf-8",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        return list(reader)


def format_registry(
    registry: list[dict[str, str]],
) -> str:
    """Convert registry rows into text for the resolver LLM."""

    headers = [
        "IT_Component",
        "Contains",
        "Project_JIRA",
        "Delivery_Team",
    ]

    lines = [
        ",".join(headers)
    ]

    for row in registry:
        lines.append(
            ",".join(
                [
                    row["IT_Component"],
                    row["Contains"],
                    row["Project_JIRA"],
                    row["Delivery_Team"],
                ]
            )
        )

    return "\n".join(lines)


@tool
def resolve_components(
    confluence_it_components: Annotated[list[str], """Complete list of IT component names extracted from the
        Confluence Engagement and Dependency page. Each list item 
        must contain exactly one IT component name. Only IT component from the confluence page should be passed, do not include
        anything else in the list"""],
) -> str:
    """
    Determine Project Jira and Delivery team for the list of IT components identified from the confluence page.
    This tool matches and resolves IT components identified from the Confluence page
    against the authoritative component registry.

    The resolver uses an LLM to identify the best matching IT_Component from the registry.
    Matched results from the registry are then returned which includes Jira project and delivery team information.
    """

    registry = load_component_registry()

    registry_text = format_registry(registry)

    model = ChatGoogleGenerativeAI(
        model="gemini-3.7-flash",
        temperature=0,
    )

    structured_model = model.with_structured_output(
        ComponentResolutionResult
    )

    prompt = f"""
You are an IT component matching engine.

Your task is to match each IT component extracted from the
Confluence page to the most appropriate IT_Component in the
provided component registry.

You have two inputs.

INPUT 1 - LIST OFIT COMPONENTS EXTRACTED FROM CONFLUENCE:

{confluence_it_components}

INPUT 2 - COMPLETE COMPONENT REGISTRY:

{registry_text}

MATCHING RULES:

1. Component Registry provided in Input 2 is authoritative.

2. You may only select an IT_Component that matches an entry
   in the registry.

3. Consider:
   - IT_Component name
   - Contains keywords
   - abbreviations
   - synonyms
   - natural language variations
   - semantic meaning

4. The Contains column contains keywords and phrases that
   may appear in the IT component names from Confluence provided as INPUT 1.

5. Never invent an IT_Component.

6. Never invent a Jira project.

7. Never invent a Delivery Team.

8. If there is no reliable match, return matched_component=null.

9. If multiple components are plausible matches, return only the one with the highest confidence and provide a brief reason for your selection.

10. Confidence must be between 0 and 1.

11. Provide a short reason for each match.

Return one match for every input component.
"""

    result = structured_model.invoke(prompt)

    # ---------------------------------------------------------
    # Resolve Jira project and delivery team from CSV.
    #
    # The LLM selects ONLY the component.
    # Python retrieves the authoritative metadata.
    # ---------------------------------------------------------

    registry_by_component = {
        row["IT_Component"]: row
        for row in registry
    }

   
    for match in result.matches:

        if match.matched_component is None or match.match_found is False:
            match.project_jira = None
            match.delivery_team = None
            continue

        row = registry_by_component.get(
            match.matched_component
        )

        if row is None:
            # Defensive check. The LLM should never produce this.
            match.matched_component = None
            match.project_jira = None
            match.delivery_team = None
            match.confidence = 0
            match.reason = (
                "The selected component was not found "
                "in the authoritative registry."
            )
            continue

        #match.project_jira = row["Project_JIRA"]
        #match.delivery_team = row["Delivery_Team"]

    return result.model_dump_json(indent=2)