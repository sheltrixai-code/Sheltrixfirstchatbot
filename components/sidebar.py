import streamlit as st


def show_sidebar():

    with st.sidebar:

        st.title("🤖 Sheltrix AI")

        st.markdown("---")

        # ----------------------------
        # New Chat
        # ----------------------------

        if st.button(
            "➕ New Chat",
            use_container_width=True
        ):

            new_chat_number = len(st.session_state.chats) + 1
            new_chat_name = f"Chat {new_chat_number}"

            st.session_state.chats[new_chat_name] = [
                {
                    "role": "assistant",
                    "content": "Hello! How can I help you today?"
                }
            ]

            st.session_state.current_chat = new_chat_name

            st.session_state.messages = (
                st.session_state.chats[new_chat_name]
            )

            st.rerun()

        st.markdown("---")

        # ----------------------------
        # Conversations
        # ----------------------------

        st.markdown("### 💬 Conversations")

        for chat_name in list(st.session_state.chats.keys()):

            if st.button(
                chat_name,
                key=f"chat_{chat_name}",
                use_container_width=True
            ):

                st.session_state.current_chat = chat_name

                st.session_state.messages = (
                    st.session_state.chats[chat_name]
                )

                st.rerun()

        # ----------------------------
        # Rename Current Chat
        # ----------------------------

        if (
            st.session_state.current_chat
            in st.session_state.chats
        ):

            with st.expander("✏️ Rename Chat"):

                new_name = st.text_input(
                    "Chat name",
                    value=st.session_state.current_chat,
                    key="rename_chat_input"
                )

                if st.button(
                    "Save Name",
                    key="save_chat_name",
                    use_container_width=True
                ):

                    new_name = new_name.strip()

                    if new_name:

                        old_name = st.session_state.current_chat

                        if new_name != old_name:

                            st.session_state.chats[new_name] = (
                                st.session_state.chats.pop(old_name)
                            )

                            st.session_state.current_chat = new_name

                            st.session_state.messages = (
                                st.session_state.chats[new_name]
                            )

                        st.rerun()

        st.markdown("---")

        # ----------------------------
        # Status
        # ----------------------------

        st.success("🟢 Status: Online")

        # ----------------------------
        # AI Model
        # ----------------------------

        st.markdown("### AI Model")

        MODELS = [
            "nvidia/nemotron-3-ultra-550b-a55b:free",
            "deepseek/deepseek-r1:free",
            "meta-llama/llama-3.3-70b-instruct:free",
            "mistralai/mistral-small-3.2-24b-instruct:free",
            "google/gemma-3-27b-it:free",
        ]

        model = st.selectbox(
            "Choose Model",
            MODELS
        )

        # ----------------------------
        # Creativity
        # ----------------------------

        st.markdown("### Creativity")

        temperature = st.slider(
            "Response Creativity",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1
        )

        # ----------------------------
        # Clear Current Chat
        # ----------------------------

        if st.button(
            "🗑️ Clear Chat",
            use_container_width=True
        ):

            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Hello! How can I help you today?"
                }
            ]

            st.session_state.chats[
                st.session_state.current_chat
            ] = st.session_state.messages

            st.rerun()

        st.markdown("---")

        st.caption("Sheltrix AI v1.0")

        return model, temperature