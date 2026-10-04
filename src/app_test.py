import uuid

import streamlit as st
from langgraph.types import Command
from langchain_core.runnables import RunnableConfig
from agent import agent


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Delivery Engagement Agent",
    page_icon="🤖",
    layout="wide",
)


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

if "agent_response" not in st.session_state:
    st.session_state.agent_response = None

if "awaiting_approval" not in st.session_state:
    st.session_state.awaiting_approval = False

if "completed" not in st.session_state:
    st.session_state.completed = False


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def get_interrupts(response):
    """
    Retrieve interrupts from the LangGraph response.

    getattr() is intentionally used because the GraphOutput
    typing in the current LangChain/LangGraph versions can
    make direct `.interrupts` access problematic in Pylance.
    """
    return getattr(response, "interrupts", None)


def get_messages(response):
    """
    Retrieve messages from the agent response.
    """

    if response is None:
        return []

    if isinstance(response, dict):
        return response.get("messages", [])

    messages = getattr(response, "messages", None)

    if messages is not None:
        return messages

    values = getattr(response, "values", None)

    if isinstance(values, dict):
        return values.get("messages", [])

    return []


def get_message_content(message):
    """
    Extract message content safely.
    """

    content = getattr(message, "content", None)

    if content is not None:
        return content

    if isinstance(message, dict):
        return message.get("content")

    return str(message)


def start_new_run():
    """
    Create a new LangGraph thread for a new engagement run.
    """

    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.agent_response = None
    st.session_state.awaiting_approval = False
    st.session_state.completed = False


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("Delivery Engagement Agent")

st.caption(
    "Analyze a Confluence engagement page and create "
    "Jira engagement tickets."
)


# ---------------------------------------------------------
# Input section
# ---------------------------------------------------------

st.subheader("Engagement Details")

confluence_url = st.text_input(
    "Confluence Engagement Page URL",
    placeholder="https://confluence.example.com/pages/12345",
)

col1, col2 = st.columns(2)

with col1:
    pi_quarter = st.text_input(
        "PI Planning Quarter",
        placeholder="PI26Q4",
    )

with col2:
    navigator_id = st.text_input(
        "Navigator ID",
        placeholder="NAV12345",
    )


# ---------------------------------------------------------
# Start analysis
# ---------------------------------------------------------

if st.button(
    "Analyze Engagement",
    type="primary",
    disabled=not confluence_url,
):

    start_new_run()

    prompt = f"""
You are an AI assistant to help IT project manager read and analyze the confluence page and raise Jira engagement tickets for the impacted components to track and deliver IT build.Read the Confluence Engagement and Dependency page.

Confluence URL:
{confluence_url}

PI Planning Quarter:
{pi_quarter}

Navigator ID:
{navigator_id}

Create Jira engagement ticket proposals for ALL impacted
IT components found on the page.

Resolve the impacted components using the component resolver.
"""

    config: RunnableConfig = {
        "configurable": {
            "thread_id": st.session_state.thread_id
        }
    }

    with st.spinner("Analyzing engagement..."):

        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ]
            },
            config=config,
        )

    st.session_state.agent_response = response

    interrupts = get_interrupts(response)

    if interrupts:
        st.session_state.awaiting_approval = True
    else:
        st.session_state.completed = True

    st.rerun()


# ---------------------------------------------------------
# Display agent activity
# ---------------------------------------------------------

response = st.session_state.agent_response

if response is not None:

    st.divider()

    st.subheader("Agent Activity")

    messages = get_messages(response)

    for message in messages:

        content = get_message_content(message)

        if not content:
            continue

        message_type = getattr(
            message,
            "type",
            "",
        )

        if message_type == "human":
            continue

        if message_type == "tool":
            with st.expander(
                "Tool result",
                expanded=False,
            ):
                st.write(content)

        else:
            with st.expander(
                "Agent message",
                expanded=False,
            ):
                st.write(content)


# ---------------------------------------------------------
# HITL approval
# ---------------------------------------------------------

if st.session_state.awaiting_approval:

    st.divider()

    st.subheader("Human Approval Required")

    st.warning(
        "The agent has prepared a batch of Jira tickets. "
        "Review the proposal before allowing ticket creation."
    )

    interrupts = get_interrupts(
        st.session_state.agent_response
    )

    if interrupts:

        with st.expander(
            "Approval details",
            expanded=True,
        ):
            st.write(interrupts)

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Approve & Create Jira Tickets",
            type="primary",
        ):

            config = {
                "configurable": {
                    "thread_id": st.session_state.thread_id
                }
            }

            with st.spinner(
                "Creating Jira tickets..."
            ):

                response = agent.invoke(
                    Command(
                        resume={
                            "decisions": [
                                {
                                    "type": "approve"
                                }
                            ]
                        }
                    ),
                    config=config,
                )

            st.session_state.agent_response = response
            st.session_state.awaiting_approval = False
            st.session_state.completed = True

            st.rerun()

    with col2:

        if st.button("Reject"):

            config = {
                "configurable": {
                    "thread_id": st.session_state.thread_id
                }
            }

            with st.spinner("Rejecting Jira creation..."):

                response = agent.invoke(
                    Command(
                        resume={
                            "decisions": [
                                {
                                    "type": "reject"
                                }
                            ]
                        }
                    ),
                    config=config,
                )

            st.session_state.agent_response = response
            st.session_state.awaiting_approval = False
            st.session_state.completed = True

            st.rerun()


# ---------------------------------------------------------
# Completion
# ---------------------------------------------------------

if st.session_state.completed:

    st.divider()

    st.success(
        "Agent workflow completed."
    )

    st.caption(
        f"Thread ID: {st.session_state.thread_id}"
    )

    if st.button("Start New Engagement"):

        start_new_run()
        st.rerun()