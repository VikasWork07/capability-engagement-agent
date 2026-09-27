from langgraph.types import Command

from agent import create_delivery_agent
from langchain_core.runnables import RunnableConfig

def print_interrupt(response):
    print("\n--- HUMAN APPROVAL REQUIRED ---")

    for interrupt in response.interrupts:
        print(interrupt)

def get_human_decision() -> str:
    """
    Simple POC decision input.
    """
    while True:
        decision = input(
            "\nEnter decision [approve/reject]: "
        ).strip().lower()

        print(f"DEBUG: received decision = {decision!r}")

        if decision in {"approve", "reject"}:
            return decision

        print("Invalid decision. Please enter approve or reject.")

def main():
    agent = create_delivery_agent()

    config: RunnableConfig = {
        "configurable": {
            "thread_id": "hitl-test-001"
        }
    }

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": """
            Process the following Confluence Engagement and Dependency page:

            https://confluence.example.com/pages/12345

            PI Quarter: PI26Q4
            Navigator ID: NAV12345
            Domain: Lending

            Read the Confluence page and create the proposed Jira engagements.

            The labels must be:

            - PI26Q4
            - NAV12345
            - Lending

"""
                }
            ]
        },
        config=config,
        version="v2",
    )

    print("\n--- Initial Result ---\n")
    print(response)

    while "__interrupt__" in response:
        
        print("\nHITL interrupt received:")
        print(response["__interrupt__"])

        decision = get_human_decision()
        print(f"\nResuming workflow with decision: {decision}")

        response = agent.invoke(
            Command(
                resume={
                    "decisions": [
                        {
                            "type": decision
                        }
                    ]
                }
            ),
            config=config,
        )

        print("\nAgent resumed.")
    print("\n--- Final Result ---\n")
    print(response)



if __name__ == "__main__":
    main()