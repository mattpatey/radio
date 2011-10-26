
import os

import random


FILES_TO_IGNORE = ['playlist']


def get_oldest_file(path, recursive=True):
    """
    Return the oldest in a given path.
    """
    files = get_files(path, recursive)
    files_with_mtime = [(f, os.stat(f).st_mtime) for f in files]
    files_sorted_by_mtime = sorted(files_with_mtime, key=lambda x: x[1])

    return files_sorted_by_mtime[0][0]

def get_random_file(path):
    """
    Return a random file from the given path.
    """
    files = get_files(path)

    return random.choice(files)

def get_files(path, recursive=True):
    """
    Return files found in a given path sorted by mtime.
    """
    files_and_dirs = os.walk(path, followlinks=True)
    file_names = list()
    if recursive:
        for files_in_dir in files_and_dirs:
            files_with_paths = [os.path.join(files_in_dir[0], f)
                                for f in files_in_dir[2] if f not in FILES_TO_IGNORE]
            file_names = file_names + files_with_paths
    else:
        for root, dirs, files in files_and_dirs:
            if root == path:
                file_names = [os.path.join(root, f) for f in files]

    return sorted(file_names, key=lambda x: os.stat(x).st_mtime)

def make_file_ancient(path):
    """
    Set a file's atime to beginning of the Unix epoch.
    """
    ancient_times = (0, 0)
    os.utime(path, ancient_times)

def make_file_brand_new(path):
    """
    Set a file's atime to now.
    """
    os.utime(path, None)

def set_playlist_mtimes(path):
    """
    Read a playlist file and sort the files within the directory
    accordingly.

    Playlist entries are expected to be relative.
    """
    order = list()
    with open(os.path.join(path, 'playlist'), 'r') as playlist:
        order = [f.rstrip('\n') for f in playlist.readlines()]
    for i, file_name in enumerate(order):
        full_path = os.path.join(path, file_name)
        atime = os.stat(full_path).st_atime
        os.utime(full_path, (atime, i))

def generate_playlist(path):
    """
    Look for a playlist file in path and generate symbolic links in
    the same directory as the playlist file.
    """
    files_to_link = list()
    with open(os.path.join(path, 'playlist'), 'r') as playlist:
        files_to_link = [f.rstrip('\n') for f in playlist.readlines()]

    for i, f in enumerate(files_to_link):
        file_name = f.split('/')[-1]
        os.symlink(f, os.path.join(path, file_name))
        atime = os.stat(f).st_atime
        os.utime(f, (atime, i))
