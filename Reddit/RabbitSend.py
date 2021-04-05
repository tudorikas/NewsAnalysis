import pika
import json
from Config.Config import config


class RabbitmqSend:
    def __init__(self):
        credentials = pika.PlainCredentials(config.IP_CONNECTION_USER, config.IP_CONNECTION_PASSWORD)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(config.IP_CONNECTION_HOST,
                                      config.IP_CONNECTION_PORT,
                                      '/',
                                      credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=config.IP_CONNECTION_QUEUE,  durable=True)



    def publish(self,data):
        jsonStr = json.dumps(data.__dict__)
        self.channel.basic_publish(exchange='', routing_key=config.IP_CONNECTION_QUEUE, body=jsonStr)



