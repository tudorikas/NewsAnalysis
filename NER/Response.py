

class Identity:
    text=None
    tag=None
    def __init__(self,text,tag):
        self.text=text
        self.tag=tag

    def to_dict(self):
        return {"text": self.text, "tag": self.tag}


class Response:
    list_identity=list()
    def __init__(self):
        pass