from http import HTTPStatus
import dashscope
import random


class Qwen:
    # documentation: https://help.aliyun.com/zh/dashscope/developer-reference/api-details
    # debug: https://dashscope.console.aliyun.com/playground?modellName=
    def __init__(self, api_key):
        dashscope.api_key = api_key

    def chat(self, user_prompt, top_p=0.7, temperature=0.1, top_k=0):
        response = dashscope.Generation.call(
            model="qwen-max",  # qwen-turbo; qwen-plus
            prompt=user_prompt,
            seed=random.randint(1, 10000),
            top_p=top_p,
            result_format="message",
            enable_search=False,
            max_tokens=1500,
            temperature=temperature,
            repetition_penalty=1.0,
            top_k=top_k,
        )
        if response.status_code == HTTPStatus.OK:
            return response["output"]["choices"][0]["message"]["content"]
        else:
            print(
                "Request id: %s, Status code: %s, error code: %s, error message: %s"
                % (
                    response.request_id,
                    response.status_code,
                    response.code,
                    response.message,
                )
            )



if __name__ == "__main__":
    api_key = ""
    qwen = Qwen(api_key)
    print(qwen.chat("你好"))
