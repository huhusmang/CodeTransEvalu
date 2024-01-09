import zhipuai
from zhipuai.model_api import model_api


class Zhipu:
    # document: https://open.bigmodel.cn/dev/api#overview
    def __init__(self, api_key):
        """
        Initializes an instance of the ZPQY class.

        Parameters:
        - api_key (str): The API key for accessing the Zhipu API.
        """
        zhipuai.api_key = api_key

    def chat(self, user_prompt, top_p=0.7, temperature=0.1):
        """
        Generates a prediction based on the given user prompt.

        Parameters:
        - user_prompt (str): The user prompt for generating the prediction.
        - top_p (float): The top-p value for controlling the randomness of the prediction. Default is 0.7.
        - temperature (float): The temperature value for controlling the randomness of the prediction. Default is 0.9.

        Returns:
        - str: The generated prediction.
        """
        response = model_api.invoke(
            model="chatglm_turbo",
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
