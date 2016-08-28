#!/usr/bin/python

import hashlib
import os

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
    dupes = find_dupes(image_path)
