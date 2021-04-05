import json

from GetNews import RedditCrawler
from RabbitSend import RabbitmqSend
from Clean import Clean
import time




with open("Folder/scann") as file:
  data = json.load(file)


#list_r=['stocks']
while True:
    news_list=list()
    new_clean_list=list()
    news=RedditCrawler()

    for channel in data:
        list_news=news.get_news(channel,data[channel])
        news_list.extend(list_news)


    for news in news_list:
        news=Clean.clean_text(news)
        if news!=None:
            new_clean_list.append(news)
    print(len(new_clean_list))
    rabbit=RabbitmqSend()
    for news in news_list:
        rabbit.publish(news)
    rabbit.channel.close()
    rabbit.connection.close()

    time.sleep(60*60)

