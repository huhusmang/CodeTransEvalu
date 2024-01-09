import os


# BaiChuan
BAICHUAN_API_KEY = os.getenv("BAICHUAN_API_KEY")

# MiniMax
MINIMAX_GROUP_ID = os.getenv("MINIMAX_GROUP_ID")
MINIMAX_SECRET_KEY = os.getenv("MINIMAX_SECRET_KEY")

# Qwen
QWEN_API_KEY = os.getenv("QWEN_API_KEY")

# Spark
SPARK_APP_ID = os.getenv("SPARK_APP_ID")
SPARK_API_KEY = os.getenv("SPARK_API_KEY")
SPARK_API_SECRET = os.getenv("SPARK_API_SECRET")

# Tiangong
TIANGONG_API_KEY = os.getenv("TIANGONG_API_KEY")
TIANGONG_SECRET_KEY = os.getenv("TIANGONG_SECRET_KEY")

# Wenxin
WENXIN_API_KEY = os.getenv("WENXIN_API_KEY")
WENXIN_SECRET_KEY = os.getenv("WENXIN_SECRET_KEY")

# Yunque
YUEQUE_VOLC_ACCESSKEY = os.getenv("YUEQUE_VOLC_ACCESSKEY")
YUEQUE_VOLC_SECERTKEY = os.getenv("YUEQUE_VOLC_SECERTKEY")

# Zhipu
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")

# ChatGLM3
CHATGLM3_API_KEY = os.getenv("CHATGLM3_API_KEY")

# GPT4
GPT4_API_KEY = os.getenv("GPT4_API_KEY")

KEY_CONFIG = {
    "baichuan_api_key": BAICHUAN_API_KEY,
    "minimax_group_id": MINIMAX_GROUP_ID,
    "minimax_secret_key": MINIMAX_SECRET_KEY,
    "qwen_api_key": QWEN_API_KEY,
    "spark_app_id": SPARK_APP_ID,
    "spark_api_key": SPARK_API_KEY,
    "spark_api_secret": SPARK_API_SECRET,
    "tiangong_api_key": TIANGONG_API_KEY,
    "tiangong_secret_key": TIANGONG_SECRET_KEY,
    "wenxin_api_key": WENXIN_API_KEY,
    "wenxin_secret_key": WENXIN_SECRET_KEY,
    "yueque_volc_accesskey": YUEQUE_VOLC_ACCESSKEY,
    "yueque_volc_secertkey": YUEQUE_VOLC_SECERTKEY,
    "zhipu_api_key": ZHIPU_API_KEY,
    "chatglm3_api_key": CHATGLM3_API_KEY,
    "gpt4_api_key": GPT4_API_KEY,
}
