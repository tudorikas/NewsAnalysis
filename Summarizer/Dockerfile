FROM python:3.7




# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

HEALTHCHECK CMD curl --fail http://172.20.0.1:5007/healthcheck || exit 1 

ENTRYPOINT [ "python" ]

CMD [ "main.py" ]