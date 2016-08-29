import sys
from oauth import oauth_login
from request import make_twitter_request
from json_tools import save_json
import argparse

def harvest_user_timeline(twitter_api, screen_name=None, user_id=None, max_results=3200):

    assert (screen_name != None) != (user_id != None), \
    "Must have screen_name or user_id, but not both"

    kw = {  # Keyword args for the Twitter API call
        'count': 200,
        'include_rts' : 'true',
        'since_id' : 1
        }

    if screen_name:
        kw['screen_name'] = screen_name
    else:
        kw['user_id'] = user_id

    max_pages = 16
    results = []

    tweets = make_twitter_request(twitter_api.statuses.user_timeline, **kw)

    if tweets is None: # 401 (Not Authorized) - Need to bail out on loop entry
        tweets = []

    results += tweets

    print('Fetched {0} tweets.'.format(len(tweets)))

    page_num = 1

    # save requests. e.g. Don't make a third request if you have 287 tweets out of
    # a possible 400 tweets after your second request. Twitter does do some
    # post-filtering on censored and deleted tweets out of batches of 'count', though,
    # so you can,w't strictly check for the number of results being 200. You might get
    # back 198, for example, and still have many more tweets to go. If you have the
    # total number of tweets for an account (by GET /users/lookup/), then you could
    # simply use this value as a guide.

    if max_results == kw['count']:
        page_num = max_pages # Prevent loop entry

    while page_num < max_pages and len(tweets) > 0 and len(results) < max_results:

        # Necessary for traversing the timeline in Twitter's v1.1 API:
        # get the next query's max-id parameter to pass in.
        # See https://dev.twitter.com/docs/working-with-timelines.
        kw['max_id'] = min([ tweet['id'] for tweet in tweets]) - 1

        tweets = make_twitter_request(twitter_api.statuses.user_timeline, **kw)
        results += tweets

        print('Fetched {0} tweets.'.format(len(tweets)))

        page_num += 1

    print('Done fetching tweets. Found {0} in total.'.format(len(results[:max_results])))

    return results[:max_results]

def tweetscrape(user, randomize=False):
    twitter_api = oauth_login(randomize)
    tweets = harvest_user_timeline(twitter_api, screen_name=user, max_results=3200)
    return tweets

if __name__ == '__main__':
    # parse cli arguments
    ap = argparse.ArgumentParser()
    ap.add_argument('-u', '--user', help = 'user to scrape (screen name or id)')
    args = vars(ap.parse_args())
    user = args['user']

    tweets = tweetscrape(user, False)
    save_json(user, tweets)
