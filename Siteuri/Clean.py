import re
import redditcleaner

class Clean:
    @staticmethod
    def clean_text(msg):
        mssg=msg.text

        text_cleaned = redditcleaner.clean(mssg)
        msg.text = text_cleaned
        if len(msg.text)>500:
            return msg
        else:
            return None