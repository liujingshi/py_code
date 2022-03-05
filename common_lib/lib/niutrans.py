from .request import Request
from .base_class import BaseClass

class NiuTransConfig:
    apikey = "414adc8121145ab49bdc146d8a9c2ec0"

class NiuTransApi:
    url = None
    method = None
    data = None

class NiuTrans(BaseClass):

    def __init__(self, **args):
        """
        默认值
        """
        self.api = None

        self._initialize()

        """
        用户传值
        """
        self._setProperty(args, "api")

    def _initialize(self):
        self.api = NiuTrans.TextApi

    def setApi(self, api):
        self.api = api

    def start(self, data = {}):
        if isinstance(data, dict):
            for k, v in data.items():
                self.api.data[k] = v
        req = Request(url=self.api.url, method=self.api.method, data=self.api.data)
        return req.start()

    class TextApi(NiuTransApi):
        url = "https://api.niutrans.com/NiuTransServer/translation"
        method = "POST"
        data = {
            "from": "en",
            "to": "zh",
            "apikey": NiuTransConfig.apikey,
            "src_text": "",
            "dictNo": "",
            "memoryNo": "",
        }
