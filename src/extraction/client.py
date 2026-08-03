import os
from pathlib import Path
from openrouter import OpenRouter
from dotenv import load_dotenv
import time

def load_api_key() -> str:
    root = Path(__file__).resolve().parents[2]
    load_dotenv(root / ".env")

    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key is None:
        raise ValueError("OPENROUTER_API_KEY not found.")

    return api_key


class LLMClient:
    def __init__(self):
        self.client = OpenRouter(api_key=load_api_key())

    def generate(self, system_prompt, user_prompt):
        # start = time.perf_counter()

        response = self.client.chat.send(
            model="openai/gpt-5-nano",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            reasoning={
                "effort": "minimal",
                "exclude": True,
            },
            max_tokens=1500,
        )
        #return response.choices[0].message.content

        # elapsed = time.perf_counter() - start
        # usage = getattr(response, "usage", None)

        # print(f"API time: {elapsed:.2f}s")
        # print(f"Model: {getattr(response, 'model', 'unknown')}")
        # print(f"Usage: {usage}")

        return response.choices[0].message.content