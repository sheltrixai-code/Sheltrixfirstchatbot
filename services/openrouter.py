import json
import requests
import streamlit as st


def get_ai_response(messages, temperature, model):
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
        "temperature": temperature,
        "stream": True
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=60,
        stream=True
    )

    response.raise_for_status()

    for line in response.iter_lines():

        if not line:
            continue

        line = line.decode("utf-8")

        if not line.startswith("data: "):
            continue

        data = line[6:]

        if data == "[DONE]":
            break

        try:
            chunk = json.loads(data)

            delta = chunk["choices"][0]["delta"]

            if "content" in delta:
                yield delta["content"]

        except Exception:
            continue