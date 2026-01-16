import json
import os
from dataclasses import dataclass

import requests


@dataclass
class FireworksClient:
    api_key: str
    model: str
    base_url: str = "https://api.fireworks.ai/inference/v1/chat/completions"

    @classmethod
    def from_env(cls):
        api_key = os.getenv("FIREWORKS_API_KEY")
        if not api_key:
            return None
        model = os.getenv(
            "FIREWORKS_MODEL",
            "accounts/fireworks/models/llama-v3-70b-instruct",
        )
        return cls(api_key=api_key, model=model)

    def complete_json(self, system_prompt, user_prompt, temperature=0.0):
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = requests.post(
            self.base_url,
            headers=headers,
            json=payload,
            timeout=20,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return None
