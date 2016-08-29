#!/usr/bin/python

import hashlib
import os
import argparse

hash_list = []
file_list = []

def find_dupes(path, cross):
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
            hash_match = hash_list[i] == hash_list[j]
            filename_i = file_list[i].split('/')[-1]
            filename_j = file_list[j].split('/')[-1]
            is_not_rt = filename_i != filename_j

            if hash_match and is_not_rt:

                def extract_user(filename):
                    #break bits up
                    chunks = filename.split('/')
                    # get last one (actual filename)
                    fn = chunks[-1]
                    # since usernames can contain _
                    # chop off the last split of a _
                    last_bit = fn.split('_')[-1]
                    user = fn.replace('_' + last_bit, '')
                    # all thats left is the user
                    return user

                def extract_id_str(filename):
                    return filename.split('/')[-1].replace('.jpg', '').split('_')[-1]

                user_i = extract_user(file_list[i])
                id_str_i = extract_id_str(file_list[i])
                user_j = extract_user(file_list[j])
                id_str_j = extract_id_str(file_list[j])
                cross_post = 'CROSS POST ' if user_i != user_j else ''

                dupes.append(file_list[j])

                # if cross post only mode and no cross, break
                if cross and cross_post == '':
                    break

                print('FOUND ' + cross_post + 'MATCH >>>')
                print('')
                print('#1 ------------- ')
                print(file_list[i])
                print('https://twitter.com/{0}/status/{1}'.format(user_i, id_str_i))
                print('')
                print('#2 ------------- ')
                print(file_list[j])
                print('https://twitter.com/{0}/status/{1}'.format(user_j, id_str_j))
                print('')
                print('~~~~~~~~~~~~~~~~~')
                print('')

    return dupes

if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    image_path = path + '/media'

    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--directory', help = 'directory to parse', default=image_path)
    ap.add_argument('-x', '--cross', help = 'only show cross post matches', action="store_true")
    args = vars(ap.parse_args())

    dupes = find_dupes(args['directory'], args['cross'])
