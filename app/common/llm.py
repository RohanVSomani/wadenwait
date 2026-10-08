import base64
import json
import os
import re

import requests


def _extract_json(text):
    if isinstance(text, dict):
        return text

    text = (text or "").strip()

    try:
        return json.loads(text)
    except Exception:
        match = re.search(
            r"\{.*\}",
            text,
            re.S,
        )

        if not match:
            raise ValueError(
                "Model did not return JSON"
            )

        return json.loads(match.group(0))


def chat_json(
    prompt,
    image_bytes,
    model=None,
    budget=120,
):
    base = os.getenv(
        "OLLAMA_URL",
        "http://127.0.0.1:11434",
    ).rstrip("/")

    model = model or os.getenv(
        "OLLAMA_MODEL",
        "qwen2.5vl:7b",
    )

    payload = {
        "model": model,
        "messages": [{
            "role": "user",
            "content": prompt,
            "images": [
                base64.b64encode(
                    image_bytes
                ).decode("ascii")
            ],
        }],
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.2,
        },
    }

    response = requests.post(
        f"{base}/api/chat",
        json=payload,
        timeout=budget,
    )

    response.raise_for_status()

    data = response.json()

    content = (
        data.get("message", {})
        .get("content", "")
    )

    return _extract_json(content), model
