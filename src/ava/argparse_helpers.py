#!/usr/bin/env python3

# Argparse validation

import argparse
import pathlib

class ValidFolder(object):
    """ Check this is a valid path - Folder """
    def __new__(cls, value):
        path = pathlib.Path(value)
        if path.exists() and path.is_dir():
            return path
        raise argparse.ArgumentTypeError(f"{value} is not a valid folder path")

class ValidFile(object):
    """ Check this is a valid path - File """
    def __new__(cls, value):
        path = pathlib.Path(value)
        if path.exists() and path.is_file():
            return path
        raise argparse.ArgumentTypeError(f"{value} is not a valid file path")
    
class ValidOutput(object):
    """ Check this is a valid path - Output """
    def __new__(cls, value):
        path = pathlib.Path(value)
        if path.parent.exists() and path.parent.is_dir():
            return path
        raise argparse.ArgumentTypeError(f"{value} is not a valid folder path. Ensure that {path.parent.name} exists")
