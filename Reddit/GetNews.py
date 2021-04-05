import requests
from Post import Post

class RedditCrawler:
    def __init__(self):
        # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
        self.auth = requests.auth.HTTPBasicAuth('vKIvRtm_D4ToWg', '7vyoEPXmGNfkKRznzBmZIfAOR71_0g')

        # here we pass our login method (password), username, and password
        self.data = {'grant_type': 'password',
                'username': 'tudorikass',
                'password': 'Securitate3395'}

        # setup our header info, which gives reddit a brief description of our app
        self.headers = {'User-Agent': 'MyBot/0.0.1'}

        # send our request for an OAuth token
        self.res = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=self.auth, data=self.data, headers=self.headers)

        # convert response to JSON and pull access_token value
        self.TOKEN = self.res.json()['access_token']

        # add authorization to our headers dictionary
    def get_news(self,channel,flairs):
        params = {'limit': 10}
        headers = {**self.headers, **{'Authorization': f"bearer {self.TOKEN}"}}

        # while the token is valid (~2 hours) we just add headers=headers to our requests
        res=requests.get('https://oauth.reddit.com/r/'+channel+'/hot', headers=headers,params=params)


        newPostList=list()
        # loop through each post retrieved from GET request
        for post in res.json()['data']['children']:
            #print(post['data']['link_flair_text'])

            if post['data']['link_flair_text'] in flairs:
                # append relevant data to dataframe
                try:
                    if post['data']['author'] != "AutoModerator":
                        newPost=Post(subreddit=post['data']['subreddit'],
                                     title=post['data']['title'],
                                     selfText=post['data']['selftext'],
                                     upvotoRatio=post['data']['upvote_ratio'],
                                     ups=post['data']['ups'],
                                     downs=post['data']['downs'],
                                     score=post['data']['score'],
                                     url=post['data']['url'],
                                     created=post['data']['created'])
                        newPostList.append(newPost)
                        #print(post['data']['selftext'])
                except Exception as ex:
                    pass

        return newPostList


