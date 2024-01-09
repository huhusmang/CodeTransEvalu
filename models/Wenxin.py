import json
import requests
import qianfan


class Wenxin:
    # document: https://cloud.baidu.com/doc/WENXINWORKSHOP/s/clntwmv7t
    def __init__(self, api_key, secret_key):
        """
        Initializes a new instance of the WXYY class.

        Args:
            api_key (str): The API key for authentication.
            secret_key (str): The secret key for authentication.
        """
        self.__api_key = api_key
        self.__secret_key = secret_key

    def get_access_token(self):
        """
        Retrieves the access token for making API requests.

        Returns:
            str: The access token.
        """
        url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={self.__api_key}&client_secret={self.__secret_key}"

        payload = json.dumps("")
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json().get("access_token")

    def chat(self, user_prompt, top_p=0.7, temperature=0.1):
        """
        Makes a prediction based on the user prompt.

        Args:
            user_prompt (str): The user prompt for the prediction.
            top_p (float, optional): The top-p value for generating the prediction. Defaults to 0.7.
            temperature (float, optional): The temperature value for generating the prediction. Defaults to 0.9.

        Returns:
            str: The predicted result.
        """
        url = (
            "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token="
            + self.get_access_token()
        )
        payload = json.dumps(
            {
                "messages": [{"role": "user", "content": user_prompt}],
                "temperature": top_p,
                "top_p": temperature,
            }
        )
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code != 200:
            print("请求失败")
            return ""

        response = response.json()
        return response["result"]


class ERNIEBot:
    # document: https://cloud.baidu.com/doc/WENXINWORKSHOP/s/xlmokikxe
    # debug: https://console.bce.baidu.com/tools/?_=1700895112895#/api?product=AI&project=%E5%8D%83%E5%B8%86%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%B9%B3%E5%8F%B0
    def __init__(self, api_key, secret_key):
        self.__api_key = api_key
        self.__secret_key = secret_key

    def chat(self, user_prompt, top_p=0.7, temperature=0.1):
        chat_comp = qianfan.ChatCompletion(ak=self.__api_key, sk=self.__secret_key)

        resp = chat_comp.do(
            model="ERNIE-Bot-4",
            messages=[{"role": "user", "content": user_prompt}],
            top_p=top_p,
            temperature=temperature,
            penalty_score=1.0,
        )

        if resp["finish_reason"] == "normal" and len(resp["result"]) > 0:
            return resp["result"]


if __name__ == "__main__":
    api_key = ""
    secret_key = ""
    wxyy = Wenxin(api_key, secret_key)
    print(wxyy.chat("你是谁"))
    erniebot = ERNIEBot(api_key, secret_key)
    print(erniebot.chat("你是谁"))
