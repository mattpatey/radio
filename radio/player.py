#!/usr/bin/env python

import ConfigParser

from optparse import OptionParser

import os

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
    config = ConfigParser.ConfigParser()
    config.read(os.path.expanduser('/home/djtanner/.python_radio'))

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
    music_library = config.get('general', 'music_lib')

    if not music_library:
        print """\
Please set 'music_lib' in the 'general' section of ~/.python_radio to
the path where your music lives."""
        sys.exit(1)

    playlists = config.get('general', 'playlists')

    if not playlists:
        print """\
Please set 'playlists' in the 'general' section of ~/.python_radio to
the path where your playlists live."""


    if options.playlist:
        playlist = os.path.join(playlists, options.playlist)
    else:
        playlist = music_library

    print get_file_to_play(playlist, random=options.shuffle)
