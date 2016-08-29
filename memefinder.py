#!/usr/bin/python

import hashlib
import os
import argparse

hash_list = []
file_list = []

def find_dupes(path):
    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(dirname, filename)
            image_file = open(file_path).read()
            hash_list.append(hashlib.md5(image_file).hexdigest())
            file_list.append(file_path)

    N = len(hash_list)
    dupes = []

    for (i,entry) in enumerate(hash_list):
        for j in range(i+1,N):
            #print i,j
            if hash_list[i] == hash_list[j]:
                print('FOUND MATCH >>> ')
                print(file_list[i])
                print(file_list[j])
                print('')
                print('~~~~~~~~~~~~~~~~~')
                print('')
                dupes.append(file_list[j])

    return dupes

if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    image_path = path + '/media'

    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--directory', help = 'directory to parse', default=image_path)
    ap.add_argument('-e', '--erase', help = 'erase dupes', action="store_true")
    args = vars(ap.parse_args())

    dupes = find_dupes(args['directory'])

    if args['erase']:
        for dupe in dupes:
            os.remove(dupe)
