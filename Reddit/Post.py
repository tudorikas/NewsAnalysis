import time

class Post:
    def __init__(self,subreddit,title,selfText,upvotoRatio,ups,downs,score,url,created):
        self.timestamp=created
        self.source="Reddit_"+subreddit
        self.title=title
        self.text=selfText
        self.upvoteRatio=upvotoRatio
        self.upsVote=ups
        self.downsVote=downs
        self.score=score
        self.url=url
        self.summarize = None
        self.keywords = None


