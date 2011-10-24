
import os

from tempfile import (
    mkdtemp,
    NamedTemporaryFile,
    )

from time import (
    sleep,
    time,
    )

from radio import player


def test_oldest_file_gets_played():
    """
    The player should return the oldest file in a folder.
    """
    tmp_folder = mkdtemp()
    assert len(os.listdir(tmp_folder)) == 0

    old_file = NamedTemporaryFile(dir=tmp_folder)
    sleep(1)
    file_to_play = player.get_file_to_play(tmp_folder)
    assert file_to_play == old_file.name

def test_play_playlist():
    """
    Passing a folder containing symlinked files should cause the
    player to return only files in that folder.
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
    linked_files = sorted(linked_files, key=lambda x: os.stat(x).st_mtime)

    assert player.get_file_to_play(linked) == linked_files[0]
    sleep(0.01)
    assert player.get_file_to_play(linked) == linked_files[1]
    sleep(0.01)
    assert player.get_file_to_play(linked) == linked_files[2]
    sleep(0.01)
    assert player.get_file_to_play(linked) == linked_files[3]
    sleep(0.01)
    assert player.get_file_to_play(linked) == linked_files[0]
