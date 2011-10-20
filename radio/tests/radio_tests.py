
from tempfile import (
    mkdtemp,
    NamedTemporaryFile,
    )

from radio.util import get_oldest_file


def test_get_oldest_file():
    """
    get_oldest_file should return the oldest file in a folder.
    """
    tmp_folder = mkdtemp()
    oldest_file = NamedTemporaryFile(dir=tmp_folder)

    assert get_oldest_file(tmp_folder) == oldest_file.name
