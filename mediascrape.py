import urllib
import argparse
import os
import io
import json
import sys
from tweetscrape import tweetscrape

def load_json(path):
    try:
        with io.open(path, encoding='utf-8') as f:
            return json.loads(f.read())
    except Exception as e:
        print('PROBLEM LOADING FILE', e)
        return []

def mediascrape(user, statuses, dump_dir, limit=None):
    all_media = []

    def add_media(status):
        status_media = status.get('entities', {}).get('media')
        screen_name = status.get('user', {}).get('screen_name')
        status_id = status.get('id_str')

        for media in status_media:
            # only get photos
            if media.get('type') != 'photo':
                break
            # dont get thumbnails
            if 'thumb' in media.get('media_url'):
                break

            all_media.append({
                    'media_url': media.get('media_url'),
                    'file_name': '{0}_{1}.jpg'.format(screen_name, status_id)
                    })


    for idx, status in enumerate(statuses):
        if limit and idx > limit:
            break

        retweeted = status.get('retweeted_status')
        if retweeted:
            tweeter = status.get('user', {}).get('id_str')
            retweeter = retweeted.get('user', {}).get('id_str')
            retweeted_media = retweeted.get('entities', {}).get('media')
            if tweeter != retweeter and retweeted_media:
                add_media(retweeted)


        status_media = status.get('entities', {}).get('media')
        if status_media:
            add_media(status)


    print('found {0} total images'.format(len(all_media)))
    for idx, media in enumerate(all_media):
        url = media.get('media_url')
        filename = media.get('file_name')
        print('fetching image {0} - {1}'.format(idx + 1, url))
        urllib.urlretrieve(url, '{0}/{1}'.format(dump_dir, filename))

if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    dump_path = path + '/media'

    # parse cli arguments
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--file', help = 'file to analyze')
    ap.add_argument('-u', '--user', help = 'user to lookup,')
    ap.add_argument('-l', '--limit', type = int, help = 'file to analyze')
    args = vars(ap.parse_args())
    user = args['user']
    limit = args['limit']
    filename = args['file']

    if user is None:
        print('PLEASE PROVIDE USER TO SCRAPE!')
        sys.exit(1)

    dump_dir = '{0}/{1}'.format(dump_path, user)
    if not os.path.exists(dump_dir):
        os.makedirs(dump_dir)

    if filename:
        statuses = load_json(filename)
    else:
        statuses = tweetscrape(user)

    mediascrape(user, statuses, dump_dir, limit)
