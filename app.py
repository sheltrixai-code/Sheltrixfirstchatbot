import streamlit as st
from components.sidebar import show_sidebar
from components.styles import load_css
from components.header import show_header
from components.chat import show_message
from services.openrouter import get_ai_response
# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Sheltrix AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)
load_css()

# ----------------------------
# Initialize Chat Sessions
# ----------------------------

if "chats" not in st.session_state:
    st.session_state.chats = {
        "Chat 1": [
            {
                "role": "assistant",
                "content": "Hello! How can I help you today?"
            }
        ]
    }

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

if "messages" not in st.session_state:
    st.session_state.messages = st.session_state.chats[
        st.session_state.current_chat
    ]

# ----------------------------
# Sidebar
# ----------------------------

model, temperature = show_sidebar()

show_header()

# Display Previous Messages
for message in st.session_state.messages:
    show_message(
        message["role"],
        message["content"]
    )

# ----------------------------
# Get User Input
# ----------------------------
if prompt := st.chat_input("Type your message..."):

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # ----------------------------
    # # Generate Chat Title
    # # ----------------------------
     
    current_chat = st.session_state.current_chat

    if current_chat.startswith("Chat "):

        title = prompt.strip()

        if len(title) > 30:
            title = title[:30].rstrip() + "..."
        st.session_state.chats[title] = st.session_state.chats.pop(

            current_chat
        )

        st.session_state.current_chat = title

    # Save user message to current chat
    
    st.session_state.chats[

        st.session_state.current_chat

    ] = st.session_state.messages

    # Show user message
    show_message("user", prompt)
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                messages = [
                    {
                        "role": "system",
                        "content": """
                        You are Sheltrix AI, a professional AI assistant
                        
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

                messages.extend(st.session_state.messages)

                placeholder = st.empty()
                full_reply = ""

                for chunk in get_ai_response(
                    messages=messages,
                    temperature=temperature,
                    model=model
                ):
                    full_reply += chunk
                    placeholder.markdown(full_reply + "▌")

                placeholder.markdown(full_reply)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": full_reply
                    }
                )

                # Save current conversation
                st.session_state.chats[
                    st.session_state.current_chat

                ] = st.session_state.messages

            except Exception as e:
                st.error(str(e))
# ----------------------------
# Sidebar
# ----------------------------
