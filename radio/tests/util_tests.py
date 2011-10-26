
import os

from tempfile import (
    mkdtemp,
    NamedTemporaryFile,
    )

from time import (
    sleep,
    time,
    )

from radio import util


def test_get_oldest_file():
    """
    get_oldest_file should return the oldest modified file in a
    folder.
    """
    tmp_folder = mkdtemp()
    old_file = NamedTemporaryFile(dir=tmp_folder)
    sleep(1)
    newest_file = NamedTemporaryFile(dir=tmp_folder)

    assert util.get_oldest_file(tmp_folder) == old_file.name

def test_get_random_file():
    """
    Get a random file from a folder.
    """
    tmp_folder = mkdtemp()
    old_file = NamedTemporaryFile(dir=tmp_folder)
    sleep(1)
    newest_file = NamedTemporaryFile(dir=tmp_folder)

    assert util.get_random_file(tmp_folder) in [old_file.name, newest_file.name]

def test_get_files():
    """
    I expect only top level files to be returned.
    """
    def make_files(path):
        files = list()
        for x in xrange(3):
            files.append(NamedTemporaryFile(dir=path))
            sleep(1)
        return files

    first_level = mkdtemp()
    first_level_files = make_files(first_level)
    second_level = mkdtemp(dir=first_level)
    second_level_files = make_files(second_level)

    all_files = first_level_files
    all_file_names = sorted([f.name for f in all_files],
                            key=lambda x: os.stat(x).st_mtime)

    assert util.get_files(first_level, recursive=False) == all_file_names

def test_get_files_ignores_files():
    tmp_folder = mkdtemp()
    music_file = NamedTemporaryFile(dir=tmp_folder)
    with open(os.path.join(tmp_folder, 'playlist'), 'w'):
        assert 2 == len(os.listdir(tmp_folder))
        assert 1 == len(util.get_files(tmp_folder))

def test_get_files_recursively():
    """
    I expect all files in a folder to be returned as a flat list,
    sorted by file modification time, from oldest to newest.
    """
    def make_files(path):
        files = list()
        for x in xrange(3):
            files.append(NamedTemporaryFile(dir=path))
            sleep(1)
        return files

    first_level = mkdtemp()
    first_level_files = make_files(first_level)
    second_level = mkdtemp(dir=first_level)
    second_level_files = make_files(second_level)
    third_level = mkdtemp(dir=second_level)
    third_level_files = make_files(third_level)

    all_files = first_level_files + second_level_files + third_level_files
    all_file_names = sorted([f.name for f in all_files],
                            key=lambda x: os.stat(x).st_mtime)

    assert util.get_files(first_level) == all_file_names

def test_follow_symlinks():
    """
    Fetching a song from a folder containing symlinks should work.
    """
    def make_files(path):
        files = list()
        for x in xrange(10):
            files.append(NamedTemporaryFile(dir=path))
            sleep(1)
        return files
    original = mkdtemp()
    files = make_files(original)
    linked = mkdtemp()
    linked_files = list()

    for f in files[:4]:
        file_name = f.name.split('/')[-1]
        link = os.path.join(linked, file_name)
        os.symlink(f.name, link)
        linked_files.append(link)

    assert set(linked_files) == set(util.get_files(linked))

def test_make_file_ancient():
    """
    make_file_ancient should set a file's atime to the beginning of
    the epoch.
    """
    tmp_folder = mkdtemp()
    tmp_file = NamedTemporaryFile(dir=tmp_folder)
    util.make_file_ancient(tmp_file.name)
    assert os.stat(tmp_file.name).st_mtime == 0.0

def test_make_file_brand_new():
    """
    make_file_brand_new should set a file's atime to now.
    """
    tmp_folder = mkdtemp()
    old_file = NamedTemporaryFile(dir=tmp_folder)
    sleep(1)
    new_file = NamedTemporaryFile(dir=tmp_folder)
    sleep(1)
    util.make_file_brand_new(old_file.name)
    assert os.stat(old_file.name).st_mtime < os.stat(new_file.name)

def test_set_playlist_with_mtime():
    """
    A playlist consists of files sorted by an input file.
    """
    tmp_folder = mkdtemp()
    files = list()
    for x in xrange(6):
        files.append(NamedTemporaryFile(dir=tmp_folder, suffix='.mp3'))
    with open(os.path.join(tmp_folder, 'playlist'), 'w') as playlist_file:
        playlist_contents = """\
%s
%s
%s
%s
%s
%s
""" % (files[2].name,
       files[1].name,
       files[4].name,
       files[0].name,
       files[3].name,
       files[5].name,)
        playlist_file.write(playlist_contents)
    files_by_mtime = [
        files[2].name,
        files[1].name,
        files[4].name,
        files[0].name,
        files[3].name,
        files[5].name,]
    util.set_playlist_mtimes(tmp_folder)

    assert files_by_mtime == util.get_files(tmp_folder)

def test_generate_playlist():
    """
    Make symbolic links from an input file.
    """
    original_folder = mkdtemp()
    original_files = list()
    for x in xrange(6):
        original_files.append(NamedTemporaryFile(dir=original_folder, suffix='.mp3'))
    playlist_folder = mkdtemp()
    with open(os.path.join(playlist_folder, 'playlist'), 'w') as playlist_file:
        playlist_contents = """\
%s
%s
%s
%s
%s
%s
""" % (original_files[2].name,
       original_files[1].name,
       original_files[4].name,
       original_files[0].name,
       original_files[3].name,
       original_files[5].name,)
        playlist_file.write(playlist_contents)
    util.generate_playlist(playlist_folder)
    sorted_files = [
        original_files[2].name,
        original_files[1].name,
        original_files[4].name,
        original_files[0].name,
        original_files[3].name,
        original_files[5].name,]
    expected_files = [f.split('/')[-1] for f in sorted_files]
    linked_files = [f.split('/')[-1] for f in util.get_files(playlist_folder)]

    assert expected_files == linked_files
