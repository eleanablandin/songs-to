import tweepy

# API twitter credentiales
all_keys = open('twitter.txt', 'r').read().splitlines()
api_key = all_keys[0]
api_key_Secret = all_keys[1]
access_token = all_keys[2]
access_token_secret = all_keys[3]

# auth with API twitter
auth = tweepy.OAuth1UserHandler(api_key, api_key_Secret)
auth.set_access_token(access_token, access_token_secret)

#obj API twitter 
api = tweepy.API(auth)

