
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

def test_get_files_recursively():
    """
    I expect all files in a folder to be returned as a flat list.
    """
    first_level = mkdtemp()
    first_level_files = [NamedTemporaryFile(dir=first_level)
                         for x in xrange(3)]
    second_level = mkdtemp(dir=first_level)
    second_level_files = [NamedTemporaryFile(dir=second_level)
                          for x in xrange(3)]
    third_level = mkdtemp(dir=second_level)
    third_level_files = [NamedTemporaryFile(dir=third_level)
                          for x in xrange(3)]
    all_files = first_level_files + second_level_files + third_level_files
    all_file_names = [f.name for f in all_files]

    assert set(util.get_files_recursively(first_level)) == set(all_file_names)

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
