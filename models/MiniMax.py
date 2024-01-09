import requests
import time


class MiniMax:
    # document: https://api.minimax.chat/document/guides/chat-pro?id=64b79fa3e74cddc5215939f4
    def __init__(self, group_id, api_key) -> None:
        self.__group_id = group_id
        self.__api_key = api_key

    def chat(self, user_prompt, top_p=0.7, temperature=0.9):
        url = f"https://api.minimax.chat/v1/text/chatcompletion_pro?GroupId={self.__group_id}"

        headers = {
            "Authorization": f"Bearer {self.__api_key}",
            "Content-Type": "application/json",
        }

        request_body = {
            "model": "abab5.5-chat",
            "tokens_to_generate": 1024,
            "top_p": top_p,
            "temperature": temperature,
            "reply_constraints": {"sender_type": "BOT", "sender_name": "MM 智能助理"},
            "messages": [
                {"sender_type": "USER", "sender_name": "用户", "text": user_prompt}
            ],
            "bot_setting": [
                {
                    "bot_name": "MM 智能助理",
                    "content": "MM 智能助理是一款由 MiniMax 自研的，没有调用其他产品的接口的大型语言模型。MiniMax 是一家中国科技公司，一直致力于进行大模型相关的研究。",
                }
            ],
        }

        retries = 0
        max_retries = 5
        while retries < max_retries:
            try:
                raw_response = requests.post(url, headers=headers, json=request_body)
                response = raw_response.json()
            except Exception as e:
                print("请求失败")
                print(f'status_code: {response["base_resp"]["status_code"]}')
                print(f'status_msg: {response["base_resp"]["status_msg"]}')
                return ""

            if response["base_resp"]["status_code"] == 1002 or response["base_resp"]["status_code"] == 1039:
                retries += 1
                if retries < max_retries:
                    wait_time = 60
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print("Max retries exceeded. Unable to complete the request.")
                    return None
            else:
                break
                
        return response["reply"]


if __name__ == "__main__":
    group_id = ""
    secret_key = ""
    api = MiniMax(group_id, secret_key)
    print(api.chat("你好，你是谁？"))
