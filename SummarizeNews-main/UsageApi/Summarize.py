import requests

from Config.Config import config
from Singleton import Singleton
from Contracts.Output import OutputNews


###return [summarize,keywords]
from UsageApi.AuxUsage import Verify


class Summarizer(metaclass=Singleton):
    def __init__(self):
        pass

    def process(self,text):
        url = config.SUMMARIZE
        new_ver = Verify()
        new_ver.text = text
        ver_json = new_ver.to_dict()
        headers = {}
        files = []
        r = requests.get(url, data=ver_json, headers=headers, timeout=100, files=files)
        if r.status_code == 200:
            print('Success!')
        elif r.status_code == 400:
            print('Not Found.')
        data = r.json()
        return [data['summarize'],data['keywords']]





#[summarize,keywords]=Summarizer().process("Tesla shares do trade at a pricey valuation, making them look like they may be significantly overvalued. Investors should consider that management expects vehicle deliveries to grow more than 50% this year. Indeed, Tesla has said it expects to sustain an average compound growth rate of about 50% for its vehicle deliveries for the foreseeable future. In addition, Tesla is now generating substantial free cash flow. This means it not only has big growth opportunities in front of it, but it can primarily fund those opportunities with internally generated cash flows.")
#a=3