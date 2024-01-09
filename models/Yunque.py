from volcengine.maas import MaasService, MaasException, ChatRole


"""
依赖安装：因为 volcengine 需要使用 C++ 构建
https://wiki.python.org/moin/WindowsCompilers
https://stackoverflow.com/questions/40504552/how-to-install-visual-c-build-tools
"""
class Yunque:
    # document: "https://www.volcengine.com/docs/82379/1099475"   "https://www.volcengine.com/docs/82379/1133189#python"
    def __init__(self, accesskey, secertkey) -> None:
        self.__access_key = accesskey
        self.__secert_key = secertkey


    def chat(self, user_prompt, top_p=0.7, temperature=0.1, top_k=0, max_tokens=1000):
        maas = MaasService("maas-api.ml-platform-cn-beijing.volces.com", "cn-beijing")

        maas.set_ak(self.__access_key)
        maas.set_sk(self.__secert_key)

        req = {
            "model": {
                "name": "skylark-pro-public",
            },
            "parameters": {
                "top_p": top_p,
                "temperature": temperature,
                "top_k": top_k,
                "max_new_tokens": max_tokens,
            },
            "messages": [{"role": ChatRole.USER, "content": user_prompt}],
        }

        try:
            resp = maas.chat(req)
            print(resp.choice.message.content)
        except MaasException as e:
            print(e)


if __name__ == "__main__":
    VOLC_ACCESSKEY = ""
    VOLC_SECRETKEY = ""
    yunque = Yunque(VOLC_ACCESSKEY, VOLC_SECRETKEY)
    yunque.chat("今天天气怎么样？")
