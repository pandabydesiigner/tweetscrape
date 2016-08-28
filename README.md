# tweetscrape

Scrapes a twitter users most recent 3200 tweets and saves to a `.json` file in `data/`. 

## Usage

Add your [twitter api](https://apps.twitter.com/) credentials to `config.json` in project root

eg:

```js
{
  "consumer_key": "XXX",
  "consumer_secret": "XXX",
  "access_token_key": "XXX",
  "access_token_secret": "XXX"
}
```

## tweetscrape

to download up to 3200 recent tweets from user: 

`python textscrape.py -u [user]`

eg: `python textscrape.py -u lilbthebasedgod`

this will save a `.json` file of tweets to `/data/[user].json`

## mediascrape

to download all media images from a user 

`python mediascrape.py -u [user]`

eg: `python mediascrape.py -u lilbthebasedgod`

this will save all files to a directory of `/media/[user]/*`

## multi\_mediascrape

_note: to use multi media scraper youll need multiple accounts as youll probably rate limit otherwise_

create an `accounts.json` in project root with the following structure:

```js
[
  {
    "consumer_key": "XXX",
    "consumer_secret": "XXX",
    "access_token_key": "XXX",
    "access_token_secret": "XXX"
  },
  {
    "consumer_key": "XXX",
    "consumer_secret": "XXX",
    "access_token_key": "XXX",
    "access_token_secret": "XXX"
  }
]
```

**if you dont have multiple accounts pass -s to just use single account**

to download all media images from a list of users, make a line-seperated `.txt` list of users and pass it to `multi_mediascrape` with `-f` 

`python multi_mediascrape.py -f [txt file of names]`

eg: `python multi_mediascrape.py -f /home/me/tweetscrape/models/names.txt`

this will save all files to a directory of `/media/[user]/*`

## Dependencies

```bash
pip install -r requirements.txt
```
