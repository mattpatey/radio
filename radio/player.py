#!/usr/bin/env python

import util


def get_file_to_play(path):
    file_to_play = util.get_oldest_file(path)
    util.make_file_brand_new(file_to_play)
    
    return file_to_play


if __name__ == '__main__':
    print get_file_to_play('/home/djtanner/radio/music/')
