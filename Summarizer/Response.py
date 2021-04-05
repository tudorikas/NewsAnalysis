
class Identity:
    summarize=None
    keywords=None

    def __init__(self,summarize,keywords):
        self.summarize=summarize
        self.keywords=keywords

    def to_dict(self):
        return {"summarize": self.summarize,"keywords":self.keywords}

