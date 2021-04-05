
from UsageApi.NERProcess import NerProcess
from UsageApi.Summarize import Summarizer
from UsageApi.Sentiment import Sentiment
from Contracts.Output import OutputNews
import copy

class ProcessNews:

    @staticmethod
    def process(news):

        ##testing
        if news.text=="":
            return None

        [probs,sentiment]=ProcessNews.sentiment(news)
        [summarize, keywords] = ProcessNews.summarize(news)
        keywords_list=ProcessNews.ner(news)
        news_output = OutputNews()
        ProcessNews.get_keywords(keywords_list, news_output)
        #keywords_bag_of_words=ProcessNews.bag_of_words(news)
        news_output.text=news.text
        news_output.title = news.title
        news_output.source = news.source
        news_output.timestamp = news.timestamp
        news_output.ticker = news.ticker
        news_output.upvoteRatio = news.upvoteRatio
        news_output.upsVote = news.upsVote
        news_output.downsVote = news.downsVote
        news_output.score = news.score
        news_output.url = news.url
        news_output.probs=probs
        news_output.sentiment=sentiment
        news_output.summarize=summarize
        return news_output

    @staticmethod
    def get_keywords(keywords_list, news_output):

        news_output.ORG=list()
        news_output.PER=list()
        news_output.MISC=list()
        news_output.LOC=list()

        for value in keywords_list['results']:
            if value['tag'] == "ORG":
                news_output.ORG.append(value['text'])
            elif value['tag'] == "PER":
                news_output.PER.append(value['text'])
            elif value['tag'] == "MISC":
                news_output.MISC.append(value['text'])
            elif value['tag'] == "LOC":
                news_output.LOC.append(value['text'])
            else:
                pass

    @staticmethod
    def bag_of_words(news):
        return BagOfWords().process(copy.copy(news.text))

    @staticmethod
    def summarize(news):
        return Summarizer().process(copy.copy(news.text))

    @staticmethod
    def sentiment(news):
        return Sentiment().process(copy.copy(news.text))

    @staticmethod
    def ner(news):
        return NerProcess().process(copy.copy(news.text))


#class n:
#    text=None
#
#aaa=n()
#aaa.text="They call it \u201cmax pain\u201d in the bitcoin options market: How to make one\u2019s trading counterparty suffer the most. Although the largest cryptocurrency was changing hands Wednesday around $56,500, traders were handicapping the odds of a plunge to about $44,000 by Friday, when a record $6 billion of options contracts is set to expire. A drop to that price level would inflict \u201cmax pain\u201d on buyers of options contracts, and it might be the most profitable price point for options sellers. It\u2019s a remote risk, but not one to be discounted. Subscribe to , By signing up, you will receive emails about CoinDesk products and you agree to our terms & conditions and privacy policy The max pain theory states that the market will gravitate toward the pain point while heading into the expiry. That\u2019s because sellers \u2013 typically institutions or sophisticated traders with ample capital supply \u2013 often try to push the price toward the max pain point by buying or selling the asset on spot or futures markets. The bullish spin is that if bitcoin makes it through Friday without a major correction, a major overhang will be lifted. \u201cMax pain for the March 26 expiry is currently $44,000 on Deribit,\u201d Luuk Strijers, CCO of Deribit, the world\u2019s largest crypto options exchange by trading volumes and open positions, told CoinDesk. \u201cThat does not mean the market will move to $44,000 by the end of this week, but it does imply that after Friday this potential downward pressure no longer exists.\u201d Bitcoin options max pain for March 26 expiry Source: Deribit Max pain is calculated by adding the outstanding put and call dollar value of each in-the-money (ITM) strike price. An ITM call is one where the strike price is below the spot market price, while a put is considered ITM when the spot market price is below the put option\u2019s strike price. A potential unwinding of trades as Friday\u2019s expiry approaches may inject some volatility into the market, according to Pankaj Balani, co-founder and CEO of Delta Exchange. Carry trading, or cash and carry arbitrage, is a market-neutral strategy that seeks to profit from increasing and decreasing prices in one or more markets. It involves buying the asset in the spot market and simultaneously selling a futures contract against it when the futures contract is trading at a significant premium to the spot price. That way, savvy traders can lock in fixed returns, as the futures price converges with the spot price on the day of expiry. \u201cWe also saw a lot of carry trades this expiry as the futures premium expanded from 15% to 25% per annum earlier this year,\u201d Balani said, adding that 60% of the short futures positions opened in carry trades are yet to be rolled over to the April expiry. Rolling over short futures means carrying over bearish positions from the current expiry to the next month. Expiry may aggravate potential sell-off The rollover, however, may not happen if the futures premium shrinks in the next two days. In simple words, carry trades will be squared off: Short futures positions will be squared off or allowed to expire, and the long positions held in the spot market could be dumped, leading to increased price volatility. Also read: This Ether Options Play by Institutions Has Lottery Ticket Potential \u201cIf the premium on futures shrinks, then we can see the unwinding of the carry trade, which can increase short-term volatility on expiry day,\u201d Balani told CoinDesk in a WhatsApp call."
#ProcessNews().process(aaa)