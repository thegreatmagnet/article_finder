import tweepy
import pandas as pd 
import datetime

#set auth tokens
auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)

#initialize tweepy, set to wait if rate limited rather than throw an exception
api = tweepy.API(auth, wait_on_rate_limit=True)

#get as many tweets as possible that contain urls
def get_tweets(query):
	tweets = []
	for t in tweepy.Cursor(api.search_tweets, q=query, include_entities=True).items():
		if len(t.entities['urls']) > 0:
			tweets.append(t)
	#get only links that aren't other tweets
	tweets = [t for t in tweets if 'twitter.com' not in t.entities['urls'][0]['expanded_url']]
	return tweets 

def build_frame(tweets):
	frame = pd.DataFrame({'user': [t.user.screen_name for t in tweets], 'date': [t.created_at.strftime('%D') for t in tweets], 'location': [t.user['location'] for t in tweets], 'text': [
		t.text for t in tweets], 'link': [t.entities['urls'][0]['expanded_url']]})
	frame.to_csv('article_links.csv')

mf_articles = get_tweets('multifamily')

build_frame(mf_articles)


