from openai import OpenAI


class GPT4:
    def __init__(self, api_key) -> None:
        self.__api_key = api_key

    def chat(self, user_prompt, temperature=0.9):
        model = "gpt-4-1106-preview"
        openai_api_key = self.__api_key
        client = OpenAI(api_key=openai_api_key)

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": user_prompt}],
            max_tokens=4096,
            seed=1239,
            temperature=temperature,
        )
        outputs = response.choices[0].message.content

        return outputs
    