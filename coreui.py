"""
Streamlit UI for the LangChain + Groq "teaching buddy" chatbot.
  
Run with:
    streamlit run app.py

Requires a .env file (or environment variables) with your Groq credentials,
e.g.:
    GROQ_API_KEY=your_key_here
"""

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# ----------------------------------------------------------------------------
# Page setup
# ----------------------------------------------------------------------------
st.set_page_config(page_title="AI Teaching Buddy", page_icon="🧑‍🏫", layout="wide")

# ----------------------------------------------------------------------------
# LLM + chains (created once, cached across reruns)
# ----------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def get_chains():
    llm = ChatGroq(model="openai/gpt-oss-120b")

    summary_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are a helpful AI assistant and teaching buddy.

Use the memory below to personalize your responses.

LONG-TERM MEMORY:
{summary}

RECENT CONVERSATION:
{history}

Instructions:
- Use long-term memory for important facts and preferences.
- Use recent conversation to maintain immediate context.
- Do not mention the memory system unless asked.
- Adapt explanations to the user's understanding level.
- If recent conversation conflicts with old memory, prefer recent information.
- Write the updated long-term memory as a concise summary paragraph.
""",
            )
        ]
    )
    summary_chain = summary_prompt | llm

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are a helpful AI assistant and teaching buddy.
Explain concepts clearly and adapt to the student's level. You also use previous memory
of a student or any person to personalise responses based on their understanding level.
Here is a previous chat summary: {summary}
Here is the recent conversation history: {history}
""",
            ),
            ("human", "{query}"),
        ]
    )
    chain = prompt | llm

    return chain, summary_chain


chain, summary_chain = get_chains()

# ----------------------------------------------------------------------------
# Session state (mirrors the original script's `history` list and `summary` str)
# ----------------------------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []  # list of {"human": ...} / {"assistant": ...}
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "messages" not in st.session_state:
    st.session_state.messages = []  # for rendering the chat UI


def history_to_text(history_list):
    """Turn the history list of dicts into a readable transcript string."""
    lines = []
    for turn in history_list:
        if "human" in turn:
            lines.append(f"Student: {turn['human']}")
        elif "assistant" in turn:
            lines.append(f"Assistant: {turn['assistant']}")
    return "\n".join(lines)


# ----------------------------------------------------------------------------
# Sidebar: long-term memory view + controls
# ----------------------------------------------------------------------------
with st.sidebar:
    st.header("🧠 Long-term memory")
    if st.session_state.summary:
        st.write(st.session_state.summary)
    else:
        st.caption("No summary yet — it builds up as the conversation grows.")

    st.divider()
    st.header("🗂️ Recent conversation buffer")
    st.caption(f"{len(st.session_state.history)} messages currently in short-term memory")

    if st.button("🔄 Reset conversation", use_container_width=True):
        st.session_state.history = []
        st.session_state.summary = ""
        st.session_state.messages = []
        st.rerun()

# ----------------------------------------------------------------------------
# Main chat UI
# ----------------------------------------------------------------------------
st.title("🧑‍🏫 AI Teaching Buddy")
st.caption("Ask anything — explanations adapt to you, with memory of past chats.")

# Render past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
query = st.chat_input("Ask your question...")

if query:
    # Show user's message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Stream the assistant's response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            for chunk in chain.stream(
                {
                    "query": query,
                    "history": history_to_text(st.session_state.history),
                    "summary": st.session_state.summary,
                }
            ):
                # ChatGroq streams AIMessageChunk objects with a .content field
                token = getattr(chunk, "content", "") or ""
                full_response += token
                placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"⚠️ Error while generating response: {e}"
            placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Update short-term history (mirrors original script)
    st.session_state.history.append({"human": query})
    st.session_state.history.append({"assistant": full_response})

    # Summarize + trim once history grows beyond 10 entries (same as original)
    if len(st.session_state.history) > 10:
        old_history = st.session_state.history[:-6]
        st.session_state.history = st.session_state.history[-6:]

        with st.spinner("Updating long-term memory..."):
            summary_response = summary_chain.invoke(
                {
                    "summary": st.session_state.summary,
                    "history": history_to_text(old_history),
                }
            )
            st.session_state.summary = summary_response.content

        st.rerun()