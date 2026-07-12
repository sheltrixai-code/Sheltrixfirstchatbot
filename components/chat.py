import streamlit as st

def show_message(role, content):
    if role == "user":
        avatar = "👤"
    else:
        avatar = "🤖"

    with st.chat_message(role, avatar=avatar):
        st.markdown(content)