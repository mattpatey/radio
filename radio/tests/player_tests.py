
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
