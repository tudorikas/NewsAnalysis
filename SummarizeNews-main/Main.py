#from RabbitConnection import Rabbitmq
#
#Rabbitmq()
import time

from RabbitConnector.RabbitConnector import RabbitConnector

while True:
    time.sleep(15)
    print("start")
    RabbitConnector().work()
    time.sleep(60)