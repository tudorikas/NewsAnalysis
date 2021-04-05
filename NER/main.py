from flask import Flask, redirect, url_for, request
from Response import Response,Identity
from Singleton import Singleton
import json
from flair.data import Sentence
from flair.models import SequenceTagger

class NER(metaclass=Singleton):
    tagger = SequenceTagger.load('ner')

app = Flask(__name__)

def make_NER(text):
    sentence = Sentence(text)

    # load the NER tagger
    a = NER()
    # run NER over sentence
    a.tagger.predict(sentence)

    new_response=list()
    # iterate over entities and print
    for entity in sentence.get_spans('ner'):
        new_entity=Identity(entity.text,entity.tag)
        new_response.append(new_entity)
    results = [obj.to_dict() for obj in new_response]
    jsdata = json.dumps({"results": results})
    return jsdata


@app.route('/healthcheck')
def hello_world():
    return 'Healthy'


@app.route('/ner',methods = ['GET'])
def login():
    text=request.form['text']
    data = make_NER(text)
    response = app.response_class(
        response=data,
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    aa = NER()
    app.run(host="0.0.0.0", port=5005)
