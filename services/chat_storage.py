import json
import os

import streamlit as st
from supabase import create_client


# ----------------------------
# Supabase Configuration
# ----------------------------

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# ----------------------------
# Local Backup File
# ----------------------------

CHAT_FILE = "data/chats.json"


# ----------------------------
# Load Chats from Supabase
# ----------------------------

def load_chats():
    """
    Load all conversations from Supabase.

    If Supabase is empty, attempt to migrate
    existing local chats.json data.
    """

    try:

        response = (
            supabase
            .table("chats")
            .select("chat_name, messages")
            .order("created_at")
            .execute()
        )

        rows = response.data or []

        chats = {
            row["chat_name"]: row["messages"]
            for row in rows
        }

        # ----------------------------
        # Migrate Existing Local Chats
        # ----------------------------

        if not chats and os.path.exists(CHAT_FILE):

            try:

                with open(
                    CHAT_FILE,
                    "r",
                    encoding="utf-8"
                ) as file:

                    local_chats = json.load(file)

                if local_chats:

                    save_chats(local_chats)

                    return local_chats

            except (
                json.JSONDecodeError,
                OSError
            ):

                pass

        return chats

    except Exception as e:

        raise RuntimeError(
            f"Unable to load chats from Supabase: {e}"
        )


# ----------------------------
# Save Chats to Supabase
# ----------------------------

def save_chats(chats):
    """
    Save all conversations to Supabase.

    Existing conversations that are no longer
    present in the application are removed.
    """

    try:

        # ----------------------------
        # Get Existing Database Chats
        # ----------------------------

        response = (
            supabase
            .table("chats")
            .select("chat_name")
            .execute()
        )

        existing_names = {
            row["chat_name"]
            for row in (response.data or [])
        }

        current_names = set(chats.keys())


        # ----------------------------
        # Delete Removed Chats
        # ----------------------------

        removed_names = (
            existing_names - current_names
        )

        if removed_names:

            supabase \
                .table("chats") \
                .delete() \
                .in_("chat_name", list(removed_names)) \
                .execute()


        # ----------------------------
        # Save Current Chats
        # ----------------------------

        if chats:

            rows = []

            for chat_name, messages in chats.items():

                rows.append(
                    {
                        "chat_name": chat_name,
                        "messages": messages
                    }
                )

            (
                supabase
                .table("chats")
                .upsert(
                    rows,
                    on_conflict="chat_name"
                )
                .execute()
            )


    except Exception as e:

        raise RuntimeError(
            f"Unable to save chats to Supabase: {e}"
        )