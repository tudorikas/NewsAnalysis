import json
import time
from random import randint

from GetNews import NewsCrawler
from RabbitSend import RabbitmqSend
from Clean import Clean
import random


#sites = ["https://www.globenewswire.com/en","https://insideevs.com/",
#         "https://www.theverge.com/", "https://finance.yahoo.com/news/"
#         "http://lite.cnn.com/en",
#         "https://www.foxbusiness.com/", "https://www.coindesk.com/"]
#
##sites=["https://www.npr.org/"]



with open("/Folder/Scan") as file:
  data = json.load(file)


#list_r=['stocks']
while True:
    news_list=list()
    new_clean_list=list()
    news=NewsCrawler()

    channel=random.choice(data['sites'])
    list_news=news.get_news(channel)
    news_list.extend(list_news)
    #time.sleep(randint(5, 15))


    for news in news_list:
        news=Clean.clean_text(news)
        if news!=None:
            new_clean_list.append(news)
    print(len(new_clean_list))
    rabbit=RabbitmqSend()
    for news in news_list:
        rabbit.publish(news)
    rabbit.connection.close()
    time.sleep(3*60)
