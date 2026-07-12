import streamlit as st
import requests
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
model, temperature = show_sidebar()
show_header()

# ----------------------------
# Initialize Chat History
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! How can I help you today?"
        }
    ]

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

    # Show user message
    show_message("user", prompt)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                messages = [
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant."
                    }
                ]

                messages.extend(st.session_state.messages)

                reply = get_ai_response(
                    messages=messages,
                    temperature=temperature,
                    model=model
                )

                st.markdown(reply)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": reply
                    }
                )

            except Exception as e:
                st.error(str(e))
# ----------------------------
# Sidebar
# ----------------------------
