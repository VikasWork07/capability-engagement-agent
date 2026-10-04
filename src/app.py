import streamlit as st
import pandas as pd
from agent import Agent


# ------------------------------------------------------------------
# Page configuration
# ------------------------------------------------------------------

st.set_page_config(
    page_title="Delivery Engagement Agent",
    page_icon="🤖",
    layout="wide",
)

st.title("Delivery Engagement Agent")


# ------------------------------------------------------------------
# Agent
# ------------------------------------------------------------------

if "engagement_agent" not in st.session_state:
    st.session_state.engagement_agent = Agent()

agent: Agent = st.session_state.engagement_agent


# ------------------------------------------------------------------
# Input
# ------------------------------------------------------------------

st.subheader("Engagement Details")

confluence_url = st.text_input(
    "Confluence Page URL",
    placeholder="https://confluence.example.com/...",
)

pi_quarter = st.text_input(
    "PI Planning Quarter",
    placeholder="PI26Q4",
)

navigator_id = st.text_input(
    "Navigator ID",
    placeholder="NAV12345",
)


# ------------------------------------------------------------------
# Start agent
# ------------------------------------------------------------------

if st.button(
    "Create Engagement Tickets",
    type="primary",
):

    if not confluence_url:
        st.error("Please enter the Confluence page URL.")

    elif not pi_quarter:
        st.error("Please enter the PI Planning Quarter.")

    elif not navigator_id:
        st.error("Please enter the Navigator ID.")

    else:

        try:

            with st.spinner(
                "Agent is processing the engagement..."
            ):

                agent.run(
                    confluence_url=confluence_url,
                    pi_quarter=pi_quarter,
                    navigator_id=navigator_id,
                )

        except Exception as exc:

            st.error(
                f"Agent execution failed: {exc}"
            )


# ------------------------------------------------------------------
# LLM response
# ------------------------------------------------------------------

if agent.output_text:

    st.divider()

    st.subheader("Agent Response")

    st.markdown(
        agent.output_text
    )


# ------------------------------------------------------------------
# Human approval
# ------------------------------------------------------------------

if agent.is_interrupted and agent.interrupt_details:

    st.divider()

    st.warning(
        "Human approval is required before Jira tickets "
        "can be created."
    )

    st.subheader("Approval Required")
    try:
        df_tickets = pd.DataFrame(agent.interrupt_details)
        st.dataframe(df_tickets)
    except Exception as exc:
        st.error(
            f"Failed to display interrupt details: {exc}"
        )
        st.json(agent.interrupt_details)
    #st.markdown(agent.interrupt_details)

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Approve",
            type="primary",
            use_container_width=True,
        ):

            try:

                with st.spinner(
                    "Creating Jira tickets..."
                ):

                    agent.resume("approve")

            except Exception as exc:

                st.error(
                    f"Agent resume failed: {exc}"
                )

    with col2:

        if st.button(
            "Reject",
            use_container_width=True,
        ):

            try:

                agent.resume("reject")

            except Exception as exc:

                st.error(
                    f"Agent resume failed: {exc}"
                )


# ------------------------------------------------------------------
# Status
# ------------------------------------------------------------------

if agent.has_active_thread:

    st.divider()

    st.caption(
        f"Thread ID: {agent.thread_id}"
    )

if agent.isCompleted:

    st.divider()

    st.success(
        "Agent has completed processing the engagement."
    )
    agent.reset_agent()
    st.rerun()