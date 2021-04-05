import re
import redditcleaner

class Clean:
    @staticmethod
    def clean_text(msg):
        mssg=msg.text
        whitespace = re.compile(r"\s+")
        web_address = re.compile(r"(?i)http(s):\/\/[a-z0-9.~_\-\/]+")
        #tesla = re.compile(r"(?i)@Tesla(?=\b)")
        user = re.compile(r"(?i)@[a-z0-9_]+")

        # we then use the sub method to replace anything matching
        mssg = whitespace.sub(' ', mssg)
        mssg = web_address.sub('', mssg)
        #mssg = tesla.sub('Tesla', mssg)
        mssg = user.sub('', mssg)


        text_cleaned = redditcleaner.clean(mssg)
        msg.text = text_cleaned
        if len(msg.text)>500:
            return msg
        else:
            return None