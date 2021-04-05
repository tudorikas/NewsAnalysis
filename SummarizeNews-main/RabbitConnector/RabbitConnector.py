import functools
import json
import threading
import pika
from Config.Config import config
from Contracts.Input import InputNews
from ElasticConnector.ElasticConnector import ElasticConnector
from ProcessNews import ProcessNews


class RabbitConnector:

    def ack_message(self,ch, delivery_tag):
        """Note that `ch` must be the same pika channel instance via which
        the message being ACKed was retrieved (AMQP protocol constraint).
        """
        if ch.is_open:
            ch.basic_ack(delivery_tag)
        else:
            # Channel is already closed, so we can't ACK this message;
            # log and/or do something that makes sense for your app in this case.
            pass


    def do_work(self,conn, ch, delivery_tag, body):
        try:
            person_dict = json.loads(body)
            news = InputNews(**person_dict)
            elastic = ElasticConnector()
            if elastic.check_exist(news.url):
                print("pass")
                pass
            else:
                news_output = ProcessNews.process(news)
                if news_output != None:
                    elastic.insert(news_output)
            cb = functools.partial(self.ack_message, ch, delivery_tag)
            conn.add_callback_threadsafe(cb)
        except Exception as ex:
            self.channel.basic_ack(delivery_tag)
            self.channel.stop_consuming()


    def on_message(self,ch, method_frame, _header_frame, body, args):
        try:
            (conn, thrds) = args
            delivery_tag = method_frame.delivery_tag
            t = threading.Thread(target=self.do_work, args=(conn, ch, delivery_tag, body))
            t.start()
            thrds.append(t)
        except Exception as ex:
            self.channel.basic_ack(delivery_tag)
            self.channel.stop_consuming()


    def work(self):
        self.credentials = pika.PlainCredentials(config.IP_CONNECTION_USER, config.IP_CONNECTION_PASSWORD)
        # Note: sending a short heartbeat to prove that heartbeats are still
        # sent even though the worker simulates long-running work
        self.parameters = pika.ConnectionParameters(
            config.IP_CONNECTION_HOST, credentials=self.credentials, heartbeat=150)
        self.connection = pika.BlockingConnection(self.parameters)

        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=config.IP_CONNECTION_QUEUE_INGEST, durable=True)

        # Note: prefetch is set to 1 here as an example only and to keep the number of threads created
        # to a reasonable amount. In production you will want to test with different prefetch values
        # to find which one provides the best performance and usability for your solution
        self.channel.basic_qos(prefetch_count=1)
        print("Connected")
        threads = []
        on_message_callback = functools.partial(self.on_message, args=(self.connection, threads))
        self.channel.basic_consume(
            queue=config.IP_CONNECTION_QUEUE_INGEST, on_message_callback=on_message_callback)

        try:
            self.channel.start_consuming()
        except Exception as ex:
            self.channel.stop_consuming()

        # Wait for all to complete
        for thread in threads:
            thread.join()

        self.connection.close()