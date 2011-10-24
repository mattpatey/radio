
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
    sleep(0.01)
    newest_file = NamedTemporaryFile(dir=tmp_folder)
    assert util.get_oldest_file(tmp_folder) == old_file.name

def test_get_files():
    """
    I expect only top level files to be returned.
    """
    def make_files(path):
        files = list()
        for x in xrange(3):
            files.append(NamedTemporaryFile(dir=path))
            sleep(0.01)
        return files

    first_level = mkdtemp()
    first_level_files = make_files(first_level)
    second_level = mkdtemp(dir=first_level)
    second_level_files = make_files(second_level)

    all_files = first_level_files
    all_file_names = sorted([f.name for f in all_files],
                            key=lambda x: os.stat(x).st_mtime)

    assert util.get_files(first_level, recursive=False) == all_file_names

def test_get_files_recursively():
    """
    I expect all files in a folder to be returned as a flat list,
    sorted by file modification time, from oldest to newest.
    """
    def make_files(path):
        files = list()
        for x in xrange(3):
            files.append(NamedTemporaryFile(dir=path))
            sleep(0.01)
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
            sleep(0.01)
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
    sleep(0.01)
    new_file = NamedTemporaryFile(dir=tmp_folder)
    sleep(0.01)
    util.make_file_brand_new(old_file.name)
    assert os.stat(old_file.name).st_mtime < os.stat(new_file.name)
