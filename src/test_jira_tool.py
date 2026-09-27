from tools.jira import create_jira_ticket


def main():
    result = create_jira_ticket.invoke(
        {
            "it_component": "Credit Decision Engine",
            "jira_project": "UNRESOLVED",
            "summary": "Expose credit decisioning API",
            "description": (
                "As a Solutions Architect for the current initiative "
                "Digital Lending Modernisation, I want the Credit "
                "Decision Engine to expose the required decisioning "
                "capability so that the lending solution can consume "
                "the credit decision.\n\n"
                "Benefit/Value:\n"
                "Enable digital lending to consume credit decisions.\n\n"
                "Work Required:\n"
                "Expose the required API.\n\n"
                "Dependencies:\n"
                "Digital Lending platform integration.\n\n"
                "Definition of Done:\n"
                "- API supports the agreed request attributes.\n"
                "- API returns the required credit decision information."
            ),
            "labels": [
                "PI26Q4",
                "NAV12345",
                "Lending",
            ],
            "dependencies": [
                "Digital Lending platform integration",
            ],
            "definition_of_done": [
                "API supports the agreed request attributes.",
                "API returns the required credit decision information.",
            ],
             "acceptance_criteria": [
                "API supports the agreed request attributes.",
                "API returns the required credit decision information.",
            ],
        }
    )

    print(result)


if __name__ == "__main__":
    main()