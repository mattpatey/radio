
import os


def get_oldest_file(path):
    """
    Return file with the smallest atime in a path.
    """
    files = [os.path.join(path, f) for f in os.listdir(path)]
    files_with_atime = [(f, os.stat(f).st_atime) for f in files]
    files_sorted_by_atime = sorted(files_with_atime, key=lambda x: x[1])

    return files_sorted_by_atime[0][0]

def make_file_ancient(path):
    """
    Set a file's atime to beginning of the Unix epoch.
    """
    ancient_times = (0, 0)
    os.utime(path, ancient_times)
