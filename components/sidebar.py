import streamlit as st

def show_sidebar():
    with st.sidebar:
        st.title("🤖 Sheltrix AI")

        st.markdown("---")

        st.success("🟢 Status: Online")

        st.markdown("### AI Model")

        model = st.selectbox(
            "Choose a model",
            [
                "nvidia/nemotron-3-ultra-550b-a55b:free"
            ]
        )

        st.markdown("### Creativity")

        temperature = st.slider(
            "Response Creativity",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1
        )

        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "How can I help you today?"
                }
            ]
            st.rerun()

        st.markdown("---")

        st.caption("Sheltrix AI v1.0")

        return model, temperature