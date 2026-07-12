import requests
import streamlit as st


def get_ai_response(messages, temperature, model):
    """
    Send chat messages to OpenRouter and return the AI response.
    """

    api_key = st.secrets["OPENROUTER_API_KEY"]

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://streamlit.io",
        "X-Title": "Sheltrix AI"
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=60
    )

    response.raise_for_status()
    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    data = response.json()

    return data["choices"][0]["message"]["content"]