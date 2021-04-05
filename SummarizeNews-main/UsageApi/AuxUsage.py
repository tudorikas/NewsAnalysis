import json


class Verify:
    text=None

    def to_dict(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))