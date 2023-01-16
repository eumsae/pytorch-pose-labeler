import os
import fnmatch


def get_files(root_dir:str, posix_regex:str, recursive:bool=True):
    """ Get the file paths that match the posix regular expression
        from root directory.
    params:
        root_dir(str): the root directory path
        posix_regex(str): posix regular expression (e.g. "*.mp4")
        recursive(bool): if true, search files recursively
    returns:
        Generator[str, None, None]: yield a file path
    """
    if not os.path.exists(root_dir):
        msg = f"{root_dir} is not exists or not a directory."
        raise ValueError(msg)
    for parent_dir, _, files in os.walk(root_dir):
        if files:  # if files are exist
            for file_ in fnmatch.filter(files, posix_regex):
                yield os.path.join(parent_dir, file_)
        if not recursive:
            break
