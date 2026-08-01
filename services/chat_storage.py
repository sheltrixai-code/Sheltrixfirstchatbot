import json
import os


CHAT_FILE = "data/chats.json"


def load_chats():
    """
    Load saved conversations from the JSON file.
    """

    if not os.path.exists(CHAT_FILE):
        return {}

    try:

        with open(CHAT_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):

        return {}


def save_chats(chats):
    """
    Save conversations to the JSON file.
    """

    os.makedirs(
        os.path.dirname(CHAT_FILE),
        exist_ok=True
    )

    with open(
        CHAT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            chats,
            file,
            indent=4,
            ensure_ascii=False
        )