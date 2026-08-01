import streamlit as st

from components.sidebar import show_sidebar
from components.styles import load_css
from components.header import show_header
from components.chat import show_message

from services.openrouter import get_ai_response
from services.chat_storage import load_chats, save_chats


# ----------------------------
# Page Configuration
# ----------------------------

st.set_page_config(
    page_title="Sheltrix AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ----------------------------
# Load Styling
# ----------------------------

load_css()


# ----------------------------
# Initialize Chat Storage
# ----------------------------

if "chats" not in st.session_state:

    saved_chats = load_chats()

    if saved_chats:

        st.session_state.chats = saved_chats

    else:

        st.session_state.chats = {
            "Chat 1": [
                {
                    "role": "assistant",
                    "content": "Hello! How can I help you today?"
                }
            ]
        }

        save_chats(st.session_state.chats)


# ----------------------------
# Initialize Current Chat
# ----------------------------

if "current_chat" not in st.session_state:

    st.session_state.current_chat = (
        next(iter(st.session_state.chats))
    )


# ----------------------------
# Load Current Messages
# ----------------------------

if "messages" not in st.session_state:

    st.session_state.messages = (
        st.session_state.chats[
            st.session_state.current_chat
        ]
    )


# ----------------------------
# Sidebar
# ----------------------------

model, temperature = show_sidebar()


# ----------------------------
# Header
# ----------------------------

show_header()


# ----------------------------
# Display Previous Messages
# ----------------------------

for message in st.session_state.messages:

    show_message(
        message["role"],
        message["content"]
    )


# ----------------------------
# Get User Input
# ----------------------------

if prompt := st.chat_input("Type your message..."):

    # ----------------------------
    # Save User Message
    # ----------------------------

    user_message = {
        "role": "user",
        "content": prompt
    }

    st.session_state.messages.append(
        user_message
    )


    # ----------------------------
    # Generate Chat Title
    # ----------------------------

    current_chat = st.session_state.current_chat

    if current_chat.startswith("Chat "):

        title = prompt.strip()

        if len(title) > 30:

            title = (
                title[:30].rstrip()
                + "..."
            )

        # Prevent empty title
        if not title:

            title = current_chat

        # Prevent duplicate title
        if (
            title != current_chat
            and title not in st.session_state.chats
        ):

            st.session_state.chats[title] = (
                st.session_state.chats.pop(
                    current_chat
                )
            )

            st.session_state.current_chat = title


    # ----------------------------
    # Save Current Chat
    # ----------------------------

    st.session_state.chats[
        st.session_state.current_chat
    ] = st.session_state.messages

    save_chats(
        st.session_state.chats
    )


    # ----------------------------
    # Show User Message
    # ----------------------------

    show_message(
        "user",
        prompt
    )


    # ----------------------------
    # Assistant Response
    # ----------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                messages = [
                    {
                        "role": "system",
                        "content": """
You are Sheltrix AI, a professional AI assistant.

Your behavior:

- Provide accurate and helpful answers.
- Explain concepts clearly and step by step.
- Be professional, friendly, and concise.
- Use Markdown formatting for readability.
- Use bullet points and numbered lists when appropriate.
- If you are uncertain, say so instead of making up information.
- For coding questions, provide complete and well-formatted code with explanations.
- Always focus on solving the user's problem efficiently.
"""
                    }
                ]


                # Add conversation history
                messages.extend(
                    st.session_state.messages
                )


                # ----------------------------
                # Streaming Response
                # ----------------------------

                placeholder = st.empty()

                full_reply = ""


                for chunk in get_ai_response(
                    messages=messages,
                    temperature=temperature,
                    model=model
                ):

                    full_reply += chunk

                    placeholder.markdown(
                        full_reply + "▌"
                    )


                # Final response
                placeholder.markdown(
                    full_reply
                )


                # ----------------------------
                # Save Assistant Message
                # ----------------------------

                assistant_message = {
                    "role": "assistant",
                    "content": full_reply
                }

                st.session_state.messages.append(
                    assistant_message
                )


                # ----------------------------
                # Save Conversation
                # ----------------------------

                st.session_state.chats[
                    st.session_state.current_chat
                ] = st.session_state.messages

                save_chats(
                    st.session_state.chats
                )


            except Exception as e:

                st.error(
                    f"Unexpected Error: {e}"
                )