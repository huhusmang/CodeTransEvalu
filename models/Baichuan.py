import json
import requests


class Baichuan:
    # documentation: https://platform.baichuan-ai.com/docs/api
    def __init__(self, api_key):
        self.__api_key = api_key

    def chat(self, user_prompt, top_p=0.7, temperature=0.1, top_k=0):
        url = "https://api.baichuan-ai.com/v1/chat/completions"

        data = {
            "model": "Baichuan2",
            "messages": [{"role": "user", "content": user_prompt}],
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
        }

        json_data = json.dumps(data)

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.__api_key,
        }

        raw_response = requests.post(url, data=json_data, headers=headers, timeout=60)
        response = raw_response.json()

        print(response)
        # {'error': {'code': 'insufficient_account_balance', 'param': None, 'type': 'rate_limit_error', 'message': 'Insufficient account balance, please recharge'}}

        if raw_response.status_code == 200:
            msg = response["choices"]["message"][0]["content"]
            return msg
        else:
            print("请求失败，状态码：", raw_response.status_code)
            print(response)
            return ""


if __name__ == "__main__":
    api_key = ""
    baichuan = Baichuan(api_key)
    print(baichuan.chat("今天天气怎么样？"))
