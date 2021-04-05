import pika


class Rabbitmq:

    def __init__(self):
        credentials = pika.PlainCredentials("tudor", "tudor")
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters("192.168.100.4",
                                      5672,
                                      '/',
                                      credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="ingest_news", durable=True)
        self.channel.queue_declare(queue="ingest_news2", durable=True)
        self.connection2 = pika.BlockingConnection(
            pika.ConnectionParameters("192.168.100.4",
                                      5672,
                                      '/',
                                      credentials))
        self.channel2 = self.connection2.channel()


        self.channel.basic_consume(
        queue="ingest_posts", on_message_callback=self.callback, auto_ack=True)

        self.channel.start_consuming()



    def callback(self,ch, method, properties, body):
        #person_dict = json.loads(body)
        self.channel.basic_publish(exchange='', routing_key="ingest_news", body=body)
        self.channel.basic_publish(exchange='', routing_key="ingest_news2", body=body)
        self.channel.basic_publish(exchange='', routing_key="news_posts", body=body)
a=Rabbitmq()
