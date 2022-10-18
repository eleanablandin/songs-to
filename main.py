from cgitb import text
from http import client
from multiprocessing.connection import Client
import tweepy

# Twitter keys
all_keys = open('twitter.txt', 'r').read().splitlines()
api_key = all_keys[0]
api_key_secret = all_keys[1]
access_token = all_keys[2]
access_token_secret = all_keys[3]

authenticator = tweepy.OAuth1UserHandler(api_key, api_key_secret)
authenticator.set_access_token(access_token, access_token_secret)

api = tweepy.API(authenticator)

api.update_status("WORKING!!")
