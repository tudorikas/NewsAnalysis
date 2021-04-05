import json

from flask import Flask, redirect, url_for, request
from summa.summarizer import summarize
from summa.keywords import keywords

from Response import Identity
from Singleton import Singleton

list_words_of_interest=list()

class Summarizer(metaclass=Singleton):
    def __init__(self):
        self.language='english'
        self.split=True
        self.ratio=0.3
        self.ratio_keywords=0.1

    def process(self,text):
        summarize=self.get_summarize(text)
        keywords=self.get_keywords(text)

        return [summarize,keywords]


    def get_summarize(self,text):
        summarized_text=summarize(text, ratio=self.ratio, language=self.language,split=self.split)
        return summarized_text

    def get_keywords(self,text):
        return keywords(text,ratio=self.ratio_keywords, split=self.split, language=self.language)


def words_in_string(word_list, a_string):
    return set(word_list).intersection(a_string.split())


def make_summarize(text):
    summ = Summarizer()
    [summarize,keywords]=summ.process(text)
    response=Identity(summarize,keywords)

    for word in words_in_string(list_words_of_interest, text):
        keywords.append(word.lower())

    results = json.dumps(response.__dict__)
    return results



app = Flask(__name__)
@app.route('/healthcheck')
def hello_world():
    return 'Healthy'


@app.route('/summarize',methods = ['GET'])
def login():
    text=request.form['text']
    data = make_summarize(text)
    response = app.response_class(
        response=data,
        status=200,
        mimetype='application/json'
    )
    return response



if __name__ == '__main__':
    with open("Nasdaqq.txt") as f:
        list_words_of_interest = f.read().splitlines()
    app.run(host="0.0.0.0", port=5007)
