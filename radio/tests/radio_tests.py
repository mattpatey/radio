
import os

from tempfile import (
    mkdtemp,
    NamedTemporaryFile,
    )

from time import (
    sleep,
    time,
    )

from radio import (
    player,
    util,
    )


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
    assert os.stat(old_file.name).st_atime < os.stat(new_file.name)

def test_get_file_to_play():
    """
    I expect get_file_to_play to return the oldest file in a folder
    and then update the file's atime to now.
    """
    tmp_folder = mkdtemp()
    old_file = NamedTemporaryFile(dir=tmp_folder)
    sleep(1)
    new_file = NamedTemporaryFile(dir=tmp_folder)
    assert player.get_file_to_play(tmp_folder) == old_file.name
    assert player.get_file_to_play(tmp_folder) == new_file.name

