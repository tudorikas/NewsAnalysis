import time

class Post:
    def __init__(self,source,title,url,text,created,ticker=""):
        self.timestamp=created
        self.source=source
        self.title = title
        self.text = text
        self.ticker = ticker
        self.url = url
        self.summarize = None
        self.keywords = None


