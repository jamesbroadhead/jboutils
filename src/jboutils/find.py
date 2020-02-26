import os
from os.path import isfile, islink
import fnmatch

from collections.abc import Iterable

def find(target, pattern=None, filters=None, _norecurse=False):
    """
    Based on:
    http://www.dabeaz.com/generators-uk/genfind.py

    @param pattern: an fnmatch pattern. If unset or None, '*'
    @param filters: a list of functions to filter result paths through
    """
    if pattern is None:
        pattern = '*'
    if filters is None:
        filters = []

    if isinstance(target, str):
        # a file or dir
        if isfile(target):
            return _find_file(target, pattern, filters) # returns a generator of strings
        return _find_dir(target, pattern, filters) # returns a generator of strings

    elif isinstance(target, Iterable):
        if _norecurse:
            raise ValueError('This method only support iterables of paths, not iterables of iterables')
        # returns a list of generators of strings or
        generators = [ find(item, pattern, filters, _norecurse=True) for item in target ]

        # flatMap - return a generator of strings
        for generator in generators:
            for item in generator:
                yield item

    raise ValueError('Must pass either a path or an iterable of paths, got {} which is a {}'.format(target, type(target)))

def _find_file(filepath, pattern, filters):
    if fnmatch.filter([filepath], pattern) and all([f(filepath) for f in filters]):
        yield filepath

def _find_dir(top_dir, pattern, filters):
    for path, _, filelist in os.walk(top_dir):
        for name in fnmatch.filter(filelist, pattern):
            full_path = os.path.join(path, name)
            if all([f(full_path) for f in filters]):
                yield full_path


def find_broken_symlinks(top_dir):
    filters = [lambda f: not isfile(f), islink]
    return find(top_dir, pattern=None, filters=filters)
