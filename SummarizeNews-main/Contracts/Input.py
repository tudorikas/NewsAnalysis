import json


class InputNews:
    def __init__(self,title,source,timestamp,text,upvoteRatio="",upsVote="",downsVote="",score="",url="",summarize="",keywords="",ticker=""):
        self.title=title
        self.source=source
        self.timestamp=timestamp
        self.text=text
        self.ticker=ticker
        self.upvoteRatio = upvoteRatio
        self.upsVote = upsVote
        self.downsVote = downsVote
        self.score = score
        self.url = url
        self.summarize = summarize
        self.keywords = keywords