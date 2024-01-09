import zhipuai
from zhipuai.model_api import model_api


class GLM3:
    # document: https://open.bigmodel.cn/dev/api#overview
    def __init__(self, api_key):
        zhipuai.api_key = api_key

    def chat(self, user_prompt, top_p=0.7, temperature=0.1):
        response = model_api.invoke(
            model="chatglm3",
            prompt=[{"role": "user", "content": user_prompt}],
            top_p=top_p,
            temperature=temperature,
        )

        if response["success"] is not True:
            print(f"Failed to get response for prompt: {user_prompt}")
            print(response)
        else:
            result = response["data"]["choices"][0]["content"]
            return result
