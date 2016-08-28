import argparse
import os
import io
import json
import sys
from tweetscrape import tweetscrape
from mediascrape import mediascrape

# set base path
path = os.path.dirname(os.path.realpath(__file__))
dump_path = path + '/media'

# parse cli arguments
ap = argparse.ArgumentParser()
ap.add_argument('-f', '--file', help = 'file of names to grab')
ap.add_argument('-l', '--limit', type = int, help = 'file to analyze')
args = vars(ap.parse_args())
filename = args['file']
limit = args['limit']

with io.open(filename, encoding='utf-8') as f:
    name_list = f.read().splitlines()

for name in name_list:
    print('SCRAPING ', name)
    dump_dir = '{0}/{1}'.format(dump_path, name)
    if not os.path.exists(dump_dir):
        os.makedirs(dump_dir)
    statuses = tweetscrape(name, randomize=True)
    mediascrape(name, statuses, dump_dir, limit)
