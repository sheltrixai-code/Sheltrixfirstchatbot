import streamlit as st

def show_header():
    st.markdown(
        """
        <div style="
            background: linear-gradient(90deg,#2563EB,#0EA5E9);
            padding:20px;
            border-radius:15px;
            margin-bottom:20px;
        ">
            <h1 style="color:white;margin:0;">
                🤖 Sheltrix AI
            </h1>
            <p style="color:white;font-size:18px;margin-top:8px;">
                Your Intelligent AI Assistant powered by OpenRouter
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )