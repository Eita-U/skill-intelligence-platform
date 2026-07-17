from openrouter import OpenRouter


class LLMClient:
    def __init__(self, api_key: str):
        self.client = OpenRouter(api_key=api_key)

    def generate(self, model, system_prompt, user_prompt):
        response = self.client.chat.send(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content