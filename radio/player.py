#!/usr/bin/env python

from optparse import OptionParser

import util


def get_file_to_play(path, random=False):
    if random:
        f = util.get_random_file
    else:
        f = util.get_oldest_file

    file_to_play = f(path)
    util.make_file_brand_new(file_to_play)

    return file_to_play


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option(
        '-p',
        '--playlist',
        help='Play music from a playlist.')
    parser.add_option(
        '-s',
        '--shuffle',
        action='store_true',
        help='Shuffle the list of songs to play.')
    parser.add_option(
        '-l',
        '--no-loop',
        action='store_false',
        help="Don't repeat the playlist after it has been played through once."
        )
    options, args = parser.parse_args()

    playlist = options.playlist or '/home/djtanner/radio/playlists/test'

    print get_file_to_play(playlist, random=options.shuffle)
