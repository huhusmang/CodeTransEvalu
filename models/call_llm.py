from .Baichuan import Baichuan
from .MiniMax import MiniMax
from .Qwen import Qwen
from .Spark import Spark
from .Tiangong import Tiangong
from .Wenxin import Wenxin, ERNIEBot
from .Yunque import Yunque
from .Zhipu import Zhipu
from .Chatglm3 import GLM3
from .GPT4 import GPT4
from .config import key_config



def call_llm(model_name):
    if model_name == "baichuan":
        return Baichuan(key_config["baichuan_api_key"])
    elif model_name == "minimax":
        return MiniMax(key_config["minimax_group_id"], key_config["minimax_secret_key"])
    elif model_name == "qwen":
        return Qwen(key_config["qwen_api_key"])
    elif model_name == "spark":
        return Spark(key_config["spark_app_id"], key_config["spark_api_key"], key_config["spark_api_secret"])
    elif model_name == "tiangong":
        return Tiangong(key_config["tiangong_api_key"], key_config["tiangong_secret_key"])
    elif model_name == "wenxin":
        return ERNIEBot(key_config["wenxin_api_key"], key_config["wenxin_secret_key"])
    elif model_name == "yunque":
        return Yunque(key_config["yueque_volc_accesskey"], key_config["yueque_volc_secertkey"])
    elif model_name == "zhipu":
        return Zhipu(key_config["zhipu_api_key"])
    elif model_name == "gpt4":
        return GPT4(key_config["gpt4_api_key"])
    elif model_name == "chatglm3":
        return GLM3(key_config["chatglm3_api_key"])
    else:
        raise ValueError(f"model_name: {model_name} is not supported.")