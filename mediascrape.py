import urllib
import argparse
import os
import io
import json
import sys
import time
from tweetscrape import tweetscrape

def load_json(path):
    try:
        with io.open(path, encoding='utf-8') as f:
            return json.loads(f.read())
    except Exception as e:
        print('PROBLEM LOADING FILE', e)
        return []

if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    dump_path = path + '/media'

    # parse cli arguments
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--file', help = 'file to analyze')
    ap.add_argument('-u', '--user', help = 'user to lookup,')
    ap.add_argument('-l', '--limit', type = int, help = 'file to analyze')
    args = vars(ap.parse_args())

    if args.get('user') is None:
        print('PLEASE PROVIDE USER TO SCRAPE!')
        sys.exit(1)

    dump_dir = '{0}/{1}'.format(dump_path, args['user'])
    if not os.path.exists(dump_dir):
        os.makedirs(dump_dir)

    if args['file']:
        statuses = load_json(args['file'])
    else:
        statuses = tweetscrape(args['user'])

    all_media = []

    def add_media(status):
        status_media = status.get('entities', {}).get('media')
        screen_name = status.get('user', {}).get('screen_name')
        status_id = status.get('id_str')

        for media in status_media:
            if media.get('type') != 'photo':
                break

            all_media.append({
                    'media_url': media.get('media_url'),
                    'file_name': '{0}_{1}.jpg'.format(screen_name, status_id)
                    })


    for idx, status in enumerate(statuses):
        if args['limit'] and idx > args['limit']:
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


    print('FOUND {0} TOTAL IMAGES'.format(len(all_media)))
    for idx, media in enumerate(all_media):
        url = media.get('media_url')
        filename = media.get('file_name')
        print('FETCHING IMAGE {0} - {1}'.format(idx, url))
        urllib.urlretrieve(url, '{0}/{1}'.format(dump_dir, filename))
