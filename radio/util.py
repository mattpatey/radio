
import os


def get_oldest_file(path, recursive=True):
    """
    Return the oldest in a given path.
    """
    files = get_files(path, recursive)
    files_with_mtime = [(f, os.stat(f).st_mtime) for f in files]
    files_sorted_by_mtime = sorted(files_with_mtime, key=lambda x: x[1])

    return files_sorted_by_mtime[0][0]

def get_files(path, recursive=True):
    """
    Return files found in a given path.
    """
    files_and_dirs = os.walk(path, followlinks=True)
    file_names = list()
    if recursive:
        for files_in_dir in files_and_dirs:
            files_with_paths = [os.path.join(files_in_dir[0], f) for f in files_in_dir[2]]
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
