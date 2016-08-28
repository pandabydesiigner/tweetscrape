# tweetscrape

Scrapes a twitter users most recent 3200 tweets and saves to a `.json` file in `data/`. 

## Usage

Add your [twitter api](https://apps.twitter.com/) credentials to oauth.py

#### tweetscrape

to download up to 3200 recent tweets from user: 

`python textscrape.py -u [user]`

eg: `python textscrape.py -u lilbthebasedgod`

this will save a `.json` file of tweets to `/data/[user].json`

#### mediascrape

to download all media images from a user 

`python mediascrape.py -u [user]`

eg: `python mediacrape.py -u lilbthebasedgod`

this will save all files to a directory of `/media/[user]/*`

## Dependencies

```bash
pip install -r requirements.txt
```
