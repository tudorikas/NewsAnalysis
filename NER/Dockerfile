FROM python:3.7




# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

COPY ./ner-english/4f4cdab26f24cb98b732b389e6cebc646c36f54cfd6e0b7d3b90b25656e4262f.8baa8ae8795f4df80b28e7f7b61d788ecbb057d1dc85aacb316f1bd02837a4a4 /root/.flair/models/ner-english/
COPY ./ner-english/4f4cdab26f24cb98b732b389e6cebc646c36f54cfd6e0b7d3b90b25656e4262f.8baa8ae8795f4df80b28e7f7b61d788ecbb057d1dc85aacb316f1bd02837a4a4.json /root/.flair/models/ner-english/

HEALTHCHECK CMD curl --fail http://172.20.0.1:5005/healthcheck || exit 1   

ENTRYPOINT [ "python" ]

CMD [ "main.py" ]