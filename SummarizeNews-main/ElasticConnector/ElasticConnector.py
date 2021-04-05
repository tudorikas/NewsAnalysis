from elasticsearch import Elasticsearch
from elasticsearch import helpers

from Config.Config import config
from Singleton import Singleton


class ElasticConnector(metaclass=Singleton):
    def __init__(self):
        self.es = Elasticsearch([config.ELASTIC_IP])

    def remove_duplicates(self,l):
        return list(set(l))

    def insert(self,news):
        #if news.timestamp==None:
        import time
        news.timestamp=int(time.time())

        doc = {
            "ORG": self.remove_duplicates(news.ORG),
            "MISC": self.remove_duplicates(news.MISC),
            "PER": self.remove_duplicates(news.PER),
            "LOC": self.remove_duplicates(news.LOC),
            "text": news.text,
            "title": news.title,
            "source": news.source,
            "timestamp": news.timestamp*1000,
            "ticker": news.ticker,
            "upvoteRatio": news.upvoteRatio,
            "upsVote": news.upsVote,
            "downsVote": news.downsVote,
            "score": news.score,
            "url": news.url,
            "probs": news.probs,
            "sentiment": news.sentiment,
            "summarize": news.summarize
        }
        #doc={
        #    "ORG": [
        #        "Microsoft",
        #        "ZeniMax",
        #        "Bethesda",
        #        "Sony"
        #    ],
        #    "MISC": [
        #        "XBOX",
        #        "PCs"
        #    ],
        #    "text": "Microsoft has closed its $7.5 billion acquisition of ZeniMax, the parent company of Bethesda. Microsoft confirmed that some new Bethesda games would be exclusive to Xbox consoles and PCs. The firm has often been seen as lagging behind Sony when it comes to major first-party releases. This is a positive news as msft could improve the gaming business. It will be more competitive to sony and able to generate more subscription revenue. The stock is trading around $230 and it is an attractive entry point for long term investors. Thanks for the awards.",
        #    "title": "Microsoft closes $7.5 billion Bethesda acquisition, aiming to take on Sony with exclusive games",
        #    "source": "Reddit_stocks",
        #    "timestamp": 1616792118000,
        #    "ticker": "",
        #    "upvoteRatio": 0.98,
        #    "upsVote": 1728,
        #    "downsVote": 0,
        #    "score": 1728,
        #    "url": "https://www.reddit.com/r/stocks/comments/mdnzup/microsoft_closes_75_billion_bethesda_acquisition/",
        #    "probs": "POSITIVE",
        #    "sentiment": "0.9437997341156006",
        #    "summarize": [
        #        "Microsoft confirmed that some new Bethesda games would be exclusive to Xbox consoles and PCs. The firm has often been seen as lagging behind Sony when it comes to major first-party releases."
        #    ]
        #}

        if self.es.exists(index=config.ELASTIC_INDEX, id=news.url):
            pass
        else:
            res = self.es.index(index=config.ELASTIC_INDEX, id=news.url, body=doc)
            print(res['result'])

    def check_exist(self,url):
        if self.es.exists(index=config.ELASTIC_INDEX, id=url):
            return True
        else:
            return False

