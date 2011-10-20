
import os

from tempfile import (
    mkdtemp,
    NamedTemporaryFile,
    )

from time import sleep

from radio import util


def test_get_oldest_file():
    """
    get_oldest_file should return the oldest file in a folder.
    """
    tmp_folder = mkdtemp()
    oldest_file = NamedTemporaryFile(dir=tmp_folder)
    sleep(1)
    kinda_new_file = NamedTemporaryFile(dir=tmp_folder)
    sleep(1)
    newest_file = NamedTemporaryFile(dir=tmp_folder)
    assert util.get_oldest_file(tmp_folder) == oldest_file.name

def test_make_file_ancient():
    """
    make_file_ancient should set a file's atime to the beginning of
    the epoch.
    """
    tmp_folder = mkdtemp()
    tmp_file = NamedTemporaryFile(dir=tmp_folder)
    util.make_file_ancient(tmp_file.name)
    assert os.stat(tmp_file.name).st_atime == 0.0
