import requests
import time
import hashlib


class Tiangong:
    # documentation: https://model-platform.tiangong.cn/api-reference
    def __init__(self, api_key, secret_key):
        """
        Initializes a new instance of the WXYY class.

        Args:
            api_key (str): The API key for authentication.
            secret_key (str): The secret key for authentication.
        """
        self.__api_key = api_key
        self.__secret_key = secret_key

    def chat(self, user_prompt, top_p=0.7, temperature=0.1, top_k=0):
        url = "https://sky-api.singularity-ai.com/saas/api/v4/generate"

        timestamp = str(int(time.time()))
        sign_content = self.__api_key + self.__secret_key + timestamp
        sign_result = hashlib.md5(sign_content.encode("utf-8")).hexdigest()

        headers = {
            "app_key": self.__api_key,
            "timestamp": timestamp,
            "sign": sign_result,
            "Content-Type": "application/json",
            "stream": "false",
        }

        data = {
            "messages": [
                {"role": "system", "content": "你是一个智能 AI 助手"},
                {"role": "user", "content": user_prompt},
            ],
            "model": "SkyChat-MegaVerse",
            "param": {
                "generate_length": 1000,
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "repetition_penalty": 1.0,
                "length_penalty": 1.0,
                "min_len": 2,
            },
        }

        raw_response = requests.post(url, headers=headers, json=data)
        response = raw_response.json()

        if (
            raw_response.status_code == 200
            and response["resp_data"]["finish_reason"] == 1
        ):
            msg = response["resp_data"]["reply"]
            return msg
        else:
            print("请求失败，状态码：", raw_response.status_code)
            print(response)
            return ""


if __name__ == "__main__":
    api_key = ""
    secret_key = ""
    tiangong = Tiangong(api_key, secret_key)
    print(tiangong.chat("你好"))
