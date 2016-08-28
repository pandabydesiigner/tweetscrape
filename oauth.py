import twitter
import io
import json
import random

def oauth_login(randomize=False):
    with io.open('config.json', encoding='utf-8') as f:
        config = json.loads(f.read())

    if randomize:
        try:
            with io.open('accounts.json', encoding='utf-8') as f:
                accounts = json.loads(f.read())

            config = random.choice(accounts)
        except Exception as e:
            print('COULDNT OPEN ACCOUNTS.JSON!')
            print(e)


    CONSUMER_KEY = config.get('consumer_key')
    CONSUMER_SECRET = config.get('consumer_secret')
    ACCESS_TOKEN = config.get('access_token_key')
    ACCESS_TOKEN_SECRET = config.get('access_token_secret')

    auth = twitter.oauth.OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api

