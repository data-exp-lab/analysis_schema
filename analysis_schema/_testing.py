import os

from yt.config import ytcfg


def yt_file_exists(req_file):
    # returns True if yt can find the file, False otherwise (a simplification of
    # yt.testing.requires_file without the nose dependency)
    path = ytcfg.get("yt", "test_data_dir")

    if os.path.exists(req_file):
        return True
    else:
        if os.path.exists(os.path.join(path, req_file)):
            return True
    return False
