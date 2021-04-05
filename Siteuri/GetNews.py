from random import randrange, randint

import newspaper
import time
import json

from Post import Post
from RabbitSend import RabbitmqSend






class NewsCrawler:
    def __init__(self):
        pass

    def get_news(self,site_crawler):
        send_article = list()

        try:
            site = newspaper.build(site_crawler, language='en', memoize_articles=False)
        except Exception as ex:
            print("Eroare la build")
            return send_article
        # get list of article URLs
        #list=site.article_urls()
        #print(len(list))
        #print(f"\n Pentru site-ul {site_crawler}:")
        if site_crawler=="http://lite.cnn.com/en":
            sites=site.articles[2:12]
        else:
            sites=site.articles[:10]
        for article in sites:
            #print(article.title)
            #continue
            try:
                article.download()
                article.parse()
            except Exception as ex:
                print("Eroare la download parse")
                continue
            #article.nlp()
            #keywords = article.keywords
            #summary = article.summary

            ticker=None
            if article.text != "":
                try:
                    ticker=article.meta_data.ticker
                except Exception as ex:
                    print("nu e ticker")
                    newArticle = Post(title=article.title, url=article.url, text=article.text,
                                         created=str(article.publish_date),source=site_crawler)
                else:
                    newArticle = Post(title=article.title,url=article.url,text=article.text,created=str(article.publish_date),ticker=ticker,source=site_crawler)
                send_article.append(newArticle)
            else:
                print("Fara text")

        return send_article
